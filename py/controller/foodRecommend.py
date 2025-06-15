from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from services.food_recommend import build_user_food_knowledge_by_category
from services.food_recommend import update_user_food_knowledge
from services.food_recommend import generate_three_meals_recommendation_r1
from controller.chat import shared_memory  # 你封装的加载模型的方法
from services.health_agent_service import init_agent
from utils.jwt import BaseContext

router = APIRouter(prefix="/foodCheckin", tags=["Food Knowledge"])

@router.post("/build")
def build_user_knowledge(db: Session = Depends(get_db)):
    user_id = BaseContext.current_user_id
    build_user_food_knowledge_by_category(user_id, db)
    return {"message": f"用户 {user_id} 的食物知识库构建完成"}


@router.post("/update")
def update_user_knowledge(db: Session = Depends(get_db)):
    user_id = BaseContext.current_user_id
    update_user_food_knowledge(user_id, db)
    return {"message": f"用户 {user_id} 的食物知识库已更新"}


@router.post("/get_recommend")
async def generate_r1_meals(db: Session = Depends(get_db)):
    user_id = BaseContext.current_user_id
    model_chain = init_agent(model="DeepSeek-R1", base_url='http://10.2.8.77:3000/v1',
                                 api_key='sk-93nWYhI8SrnXad5m9932CeBdDeDf4233B21d93D217095f22', memory=shared_memory)

    result = await generate_three_meals_recommendation_r1(user_id, db, model_chain)
    return result


