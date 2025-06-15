from fastapi import APIRouter, Request, HTTPException, status, UploadFile, File, Depends

from utils.encryption import encrypt_content, decrypt_content
from utils.jwt import BaseContext
from models.database import get_db, UserKnowledgeFile
from services.knowledge_manager import knowledge_manager
from config.knowledge_config import config
from sqlalchemy.orm import Session
import os
import shutil

router = APIRouter(prefix="/knowledge/file", tags=["knowledge_file"])


@router.get("/list")
async def list_knowledge_files(db: Session = Depends(get_db)):
    """获取用户的知识库文件列表"""
    user_id = BaseContext.current_user_id
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )

    try:
        files = db.query(UserKnowledgeFile).filter(
            UserKnowledgeFile.user_id == user_id,
            UserKnowledgeFile.status == "active"
        ).order_by(UserKnowledgeFile.created_at.desc()).all()

        file_list = [
            {
                "id": file.id,
                "file_name": file.file_name,
                "file_size": file.file_size,
                "file_type": file.file_type,
                "source_type": file.source_type,
                "chunk_count": file.chunk_count,
                "created_at": file.created_at.isoformat(),
                "updated_at": file.updated_at.isoformat() if file.updated_at else None,
                "status": file.status
            }
            for file in files
        ]

        return {"files": file_list}
    except Exception as e:
        print(f"获取文件列表时出错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get file list: {str(e)}"
        )


@router.delete("/{file_id}")
async def delete_knowledge_file(file_id: int, db: Session = Depends(get_db)):
    """删除知识库文件 - 使用统一管理服务"""
    user_id = BaseContext.current_user_id
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )

    try:
        # 使用统一管理服务删除文档
        result = knowledge_manager.delete_document(user_id, file_id, db)

        if result["success"]:
            db.commit()
            return {
                "message": "File deleted successfully",
                "details": {
                    "file_id": result["file_id"],
                    "vector_ids_deleted": len(result["vector_ids_deleted"]),
                    "file_deleted": result["file_deleted"]
                }
            }
        else:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete file: {result['error']}"
            )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"删除文件时出错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """上传文件到个人知识库 - 使用统一管理服务"""
    # 获取当前用户ID
    user_id = BaseContext.current_user_id
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )

    try:
        # 检查文件类型
        if not config.is_supported_file_type(file.filename):
            file_ext = os.path.splitext(file.filename)[1].lower()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type: {file_ext}. Allowed: {', '.join(config.SUPPORTED_EXTENSIONS)}"
            )

        # 检查文件大小
        file_size = 0
        content = await file.read()
        file_size = len(content)
        await file.seek(0)  # 重置文件指针

        if not config.validate_file_size(file_size):
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Maximum size: {config.get_file_size_limit_mb()}MB"
            )

        # 生成唯一的文件名
        unique_filename = f"{user_id}_{file.filename}"
        file_path = os.path.join(config.UPLOAD_DIR, unique_filename)
        print(f"开始处理用户 {user_id} 的文件上传: {file.filename}")

        # 保存文件
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 新增：立即加密文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        encrypted_content = encrypt_content(content, user_id)
        encrypted_file_path = file_path + '.enc'
        with open(encrypted_file_path, 'w', encoding='utf-8') as f:
            f.write(encrypted_content)

        # 删除原始文件
        os.remove(file_path)
        file_path = encrypted_file_path

        print(f"加密文件已保存到: {file_path}")

        # 使用统一管理服务添加文档
        result = knowledge_manager.add_document(
            user_id=user_id,
            file_path=file_path,
            file_name=file.filename,
            file_type=file.content_type or "application/octet-stream",
            source_type="uploaded_file",
            db=db
        )

        if result["success"]:
            db.commit()
            print(f"文件处理完成: {file.filename}")
            return {
                "message": "File uploaded and processed successfully",
                "details": {
                    "file_id": result["file_id"],
                    "chunk_count": result["chunk_count"],
                    "file_size": result["file_size"]
                }
            }
        else:
            # 清理上传的文件
            if os.path.exists(file_path):
                os.remove(file_path)
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to process file: {result['error']}"
            )

    except HTTPException:
        # 清理上传的文件
        if os.path.exists(file_path):
            os.remove(file_path)
        raise
    except Exception as e:
        # 清理上传的文件
        if os.path.exists(file_path):
            os.remove(file_path)
        db.rollback()
        print(f"处理文件时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        )


@router.post("/sync")
async def sync_knowledge_base(db: Session = Depends(get_db)):
    """同步知识库，检查并修复数据不一致问题"""
    user_id = BaseContext.current_user_id
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )

    try:
        result = knowledge_manager.sync_user_knowledge(user_id, db)
        return {
            "message": "Knowledge base sync completed",
            "result": result
        }
    except Exception as e:
        print(f"同步知识库时出错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sync knowledge base: {str(e)}"
        )


@router.get("/decrypt/{file_id}")
async def get_decrypted_content(file_id: int, db: Session = Depends(get_db)):
    """获取解密后的文件内容（仅用于调试，生产环境慎用）"""
    user_id = BaseContext.current_user_id
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    file_record = db.query(UserKnowledgeFile).filter(
        UserKnowledgeFile.id == file_id,
        UserKnowledgeFile.user_id == user_id,
        UserKnowledgeFile.status == "active"
    ).first()

    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(file_record.file_path, 'r', encoding='utf-8') as f:
            encrypted_content = f.read()

        decrypted_content = decrypt_content(encrypted_content, user_id)
        return {"content": decrypted_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decryption failed: {str(e)}")