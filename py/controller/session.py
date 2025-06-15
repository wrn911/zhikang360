from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from models.database import get_db, ChatSession, ChatHistory
from utils.jwt import BaseContext
from pydantic import BaseModel

# ==== 新增：智能体配置 ====
AGENTS = {
    "general": {
        "name": "健康助手",
        "icon": "🏥",
        "description": "提供全面的健康咨询"
    },
    "nutritionist": {
        "name": "营养师",
        "icon": "🥗",
        "description": "专业营养指导"
    },
    "trainer": {
        "name": "健身教练",
        "icon": "💪",
        "description": "运动健身指导"
    },
    "psychologist": {
        "name": "心理咨询师",
        "icon": "🧠",
        "description": "心理健康支持"
    }
}
router = APIRouter(prefix="/session", tags=["session"])

class SessionCreate(BaseModel):
    title: str

class SessionResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int

@router.post("/create")
async def create_session(request: SessionCreate):
    """创建新会话"""
    user_id = BaseContext.current_user_id
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
    
    db = next(get_db())
    try:
        session = ChatSession(
            user_id=user_id,
            title=request.title
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return {"message": "Session created successfully", "session_id": session.id}
    finally:
        db.close()


@router.get("/list")
async def list_sessions():
    """获取用户的所有会话"""
    user_id = BaseContext.current_user_id
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )

    db = next(get_db())
    try:
        sessions = db.query(ChatSession).filter(
            ChatSession.user_id == user_id
        ).order_by(ChatSession.updated_at.desc()).all()

        # 获取每个会话的消息数量和智能体信息
        session_list = []
        for session in sessions:
            message_count = db.query(ChatHistory).filter(
                ChatHistory.session_id == session.id
            ).count()

            # ==== 新增：获取智能体信息 ====
            agent_id = getattr(session, 'agent_id', 'general')
            agent_info = AGENTS.get(agent_id, AGENTS['general'])

            session_list.append({
                "id": session.id,
                "title": session.title,
                "agent_id": agent_id,  # 新增
                "agent_name": agent_info["name"],  # 新增
                "agent_icon": agent_info["icon"],  # 新增
                "created_at": session.created_at,
                "updated_at": session.updated_at,
                "message_count": message_count
            })

        return {"sessions": session_list}
    finally:
        db.close()

@router.get("/{session_id}/history")
async def get_session_history(session_id: int, page: int = 1, page_size: int = 10):
    """获取指定会话的历史记录"""
    user_id = BaseContext.current_user_id
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
    
    db = next(get_db())
    try:
        # 验证会话所有权
        session = db.query(ChatSession).filter(
            ChatSession.id == session_id,
            ChatSession.user_id == user_id
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # 获取历史记录总数
        total = db.query(ChatHistory).filter(
            ChatHistory.session_id == session_id
        ).count()
        
        # 获取分页历史记录
        histories = db.query(ChatHistory).filter(
            ChatHistory.session_id == session_id
        ).order_by(ChatHistory.created_at.asc())\
         .offset((page - 1) * page_size)\
         .limit(page_size)\
         .all()
        
        # 转换为所需格式
        history_list = [
            {
                "question": item.question,
                "answer": item.answer,
                "timestamp": item.created_at.isoformat()
            }
            for item in histories
        ]
        
        return {
            "history": history_list,
            "total": total,
            "page": page,
            "page_size": page_size
        }
    finally:
        db.close()

@router.delete("/{session_id}")
async def delete_session(session_id: int):
    """删除会话及其历史记录"""
    user_id = BaseContext.current_user_id
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
    
    db = next(get_db())
    try:
        # 验证会话所有权
        session = db.query(ChatSession).filter(
            ChatSession.id == session_id,
            ChatSession.user_id == user_id
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # 删除会话及其历史记录
        db.query(ChatHistory).filter(ChatHistory.session_id == session_id).delete()
        db.delete(session)
        db.commit()
        
        return {"message": "Session deleted successfully"}
    finally:
        db.close() 