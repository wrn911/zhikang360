from fastapi import APIRouter, HTTPException, status, UploadFile, File
from services.knowledge_manager import knowledge_manager
from config.knowledge_config import config
from pydantic import BaseModel
from typing import Optional
import os

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


class GlobalKnowledgeLoadRequest(BaseModel):
    data_directory: Optional[str] = None
    force_reload: Optional[bool] = False


@router.post("/global/load")
async def load_global_knowledge_endpoint(request: GlobalKnowledgeLoadRequest = GlobalKnowledgeLoadRequest()):
    """
    加载全局知识库
    支持指定数据目录和强制重新加载
    """
    try:
        # 如果强制重新加载，先清空现有知识库
        if request.force_reload:
            clear_result = knowledge_manager.clear_global_knowledge()
            if not clear_result["success"]:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to clear existing knowledge base: {clear_result['error']}"
                )

        # 加载全局知识库
        result = knowledge_manager.load_global_knowledge(request.data_directory)

        if result["success"]:
            return {
                "message": "Global knowledge base loaded successfully",
                "details": {
                    "documents_loaded": result["documents_loaded"],
                    "chunks_created": result["chunks_created"],
                    "files_processed": result["files_processed"],
                    "data_directory": result["data_directory"]
                }
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("message", result.get("error", "Unknown error"))
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/global/add-file")
async def add_file_to_global_knowledge(file: UploadFile = File(...)):
    """
    向全局知识库添加单个文件
    """
    try:
        # 检查文件类型
        if not config.is_supported_file_type(file.filename):
            file_ext = os.path.splitext(file.filename)[1].lower()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type: {file_ext}. Allowed: {', '.join(config.SUPPORTED_EXTENSIONS)}"
            )

        # 临时保存文件
        temp_file_path = os.path.join(config.TEMP_DIR, file.filename)

        try:
            # 保存上传的文件
            import shutil
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # 添加到全局知识库
            result = knowledge_manager.add_to_global_knowledge(temp_file_path, file.filename)

            if result["success"]:
                return {
                    "message": "File added to global knowledge base successfully",
                    "details": {
                        "file_name": result["file_name"],
                        "chunks_added": result["chunks_added"]
                    }
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to add file: {result['error']}"
                )

        finally:
            # 清理临时文件
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.delete("/global/clear")
async def clear_global_knowledge():
    """
    清空全局知识库
    """
    try:
        result = knowledge_manager.clear_global_knowledge()

        if result["success"]:
            return {
                "message": "Global knowledge base cleared successfully"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to clear global knowledge base: {result['error']}"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/global/stats")
async def get_global_knowledge_stats():
    """
    获取全局知识库统计信息
    """
    try:
        result = knowledge_manager.get_global_knowledge_stats()

        if result["success"]:
            return {
                "message": "Global knowledge base statistics retrieved successfully",
                "stats": {
                    "total_documents": result["total_documents"],
                    "unique_sources": result.get("unique_sources", 0),
                    "file_types": result.get("file_types", {}),
                    "sources": result.get("sources", [])
                }
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get statistics: {result['error']}"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


# 保持向后兼容的端点
@router.post("/loadGlobal")
async def load_global_knowledge_legacy():
    """加载全局知识库 - 向后兼容的端点"""
    try:
        result = knowledge_manager.load_global_knowledge()
        if result["success"]:
            return {"message": "Global knowledge base loaded successfully"}
        else:
            return {"message": f"Failed to load global knowledge base: {result.get('error', 'Unknown error')}"}
    except Exception as e:
        return {"message": f"Failed to load global knowledge base: {str(e)}"}