from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from models.database import get_db, User, UserKnowledgeStatus
from services.user_knowledge_updater import create_update_task, update_user_health_knowledge
from utils.jwt import BaseContext
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/health-data", tags=["health_data_sync"])


class SyncRequest(BaseModel):
    force_update: Optional[bool] = False  # 是否强制立即更新


@router.post("/sync/{user_id}")
async def sync_user_health_data(
        user_id: int,
        request: SyncRequest = SyncRequest(),
        db: Session = Depends(get_db)
):
    """
    接收Java后端的健康数据更新通知
    创建知识库更新任务
    """
    try:
        # 验证用户是否存在
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if request.force_update:
            # 强制立即更新
            print(f"强制立即更新用户 {user_id} 的知识库")
            success = update_user_health_knowledge(user_id, db)
            if success:
                return {
                    "message": "Health knowledge updated successfully",
                    "user_id": user_id,
                    "update_type": "immediate"
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update health knowledge"
                )
        else:
            # 创建异步更新任务
            success = create_update_task(user_id, db)
            if success:
                return {
                    "message": "Health data sync task created successfully",
                    "user_id": user_id,
                    "update_type": "async"
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create update task"
                )

    except HTTPException:
        raise
    except Exception as e:
        print(f"同步用户 {user_id} 健康数据时出错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/refresh")
async def refresh_current_user_knowledge(
        request: SyncRequest = SyncRequest(),
        db: Session = Depends(get_db)
):
    """
    手动刷新当前用户的知识库
    """
    user_id = BaseContext.current_user_id
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )

    try:
        if request.force_update:
            # 立即更新
            success = update_user_health_knowledge(user_id, db)
            if success:
                return {
                    "message": "Knowledge base refreshed successfully",
                    "user_id": user_id,
                    "update_type": "immediate"
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to refresh knowledge base"
                )
        else:
            # 创建任务
            success = create_update_task(user_id, db)
            if success:
                return {
                    "message": "Knowledge refresh task created successfully",
                    "user_id": user_id,
                    "update_type": "async"
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create refresh task"
                )

    except HTTPException:
        raise
    except Exception as e:
        print(f"刷新用户 {user_id} 知识库时出错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/status")
async def get_knowledge_status(db: Session = Depends(get_db)):
    """
    获取当前用户的知识库状态
    """
    user_id = BaseContext.current_user_id
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )

    try:
        status_record = db.query(UserKnowledgeStatus).filter(
            UserKnowledgeStatus.user_id == user_id
        ).first()

        if not status_record:
            return {
                "user_id": user_id,
                "has_health_profile": False,
                "update_status": "not_initialized",
                "last_health_update": None,
                "last_knowledge_update": None
            }

        # 检查健康档案文件是否存在
        import os
        has_profile = (status_record.health_profile_path and
                       os.path.exists(status_record.health_profile_path))

        return {
            "user_id": user_id,
            "has_health_profile": has_profile,
            "health_profile_path": status_record.health_profile_path,
            "update_status": status_record.update_status,
            "last_health_update": status_record.last_health_update.isoformat() if status_record.last_health_update else None,
            "last_knowledge_update": status_record.last_knowledge_update.isoformat() if status_record.last_knowledge_update else None,
            "created_at": status_record.created_at.isoformat() if status_record.created_at else None,
            "updated_at": status_record.updated_at.isoformat() if status_record.updated_at else None
        }

    except Exception as e:
        print(f"获取用户 {user_id} 知识库状态时出错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )