from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from services.exercise_checkin import (
    build_user_exercise_knowledge_by_category,
    update_user_exercise_knowledge,
    generate_three_exercise_recommendation_r1
)
from controller.chat import shared_memory
from services.health_agent_service import init_agent
from utils.jwt import BaseContext

router = APIRouter(prefix="/exerciseCheckin", tags=["Exercise Knowledge"])

@router.post("/build")
def build_exercise_knowledge(db: Session = Depends(get_db)):
    user_id = BaseContext.current_user_id
    build_user_exercise_knowledge_by_category(user_id, db)
    return {"message": f"用户 {user_id} 的运动知识库构建完成"}

@router.post("/update")
def update_exercise_knowledge(db: Session = Depends(get_db)):
    user_id = BaseContext.current_user_id
    update_user_exercise_knowledge(user_id, db)
    return {"message": f"用户 {user_id} 的运动知识库已更新"}

@router.post("/get_recommend")
async def generate_r1_exercise_recommendation(db: Session = Depends(get_db)):
    user_id = BaseContext.current_user_id
    model_chain = init_agent(
        model="DeepSeek-R1",
        base_url='http://10.2.8.77:3000/v1',
        api_key='sk-93nWYhI8SrnXad5m9932CeBdDeDf4233B21d93D217095f22',
        memory=shared_memory
    )
    result = await generate_three_exercise_recommendation_r1(user_id, db, model_chain)
    return result
