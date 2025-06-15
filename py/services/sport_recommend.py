from langchain_core.prompts import ChatPromptTemplate

from models.database import (
    get_db, SportInfo, UserInfo, IllnessInfo, ExerciseCheckin, Exercise, UserRecommendInfo
)
from services.feedback_services import load_user_vectorstore
from services.food_services import get_food_rag_chain, load_food_vectorstore
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
import json
from langchain_huggingface import HuggingFaceEmbeddings
import asyncio

# 请求结构体
from datetime import datetime, timedelta

from services.sport_services import get_sport_rag_chain, load_exercise_vectorstore


def get_recent_feedback_context(user_id: int, days: int = 12):
    vectorstore = load_user_vectorstore(user_id)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    docs = retriever.get_relevant_documents("最近的运动反馈")

    threshold = datetime.now() - timedelta(days=days)
    recent_docs = [
        doc for doc in docs
        if "date" in doc.metadata and str(doc.metadata["date"]) >= str(threshold.date())
    ]

    if not recent_docs:
        return "无"

    extracted_feedbacks = []
    for doc in recent_docs:
        date_str = str(doc.metadata.get("date", "未知时间"))
        for line in doc.page_content.splitlines():
            if "运动反馈：" in line:
                feedback = line.replace("运动反馈：", "").strip()
                if feedback:
                    extracted_feedbacks.append(f"{date_str}：{feedback}")

    return "\n".join(extracted_feedbacks) if extracted_feedbacks else "无"


async def generate_exercise_recommendation(user_id: int):
    db: Session = next(get_db())

    # 获取用户信息
    sport_info = db.query(SportInfo).filter(SportInfo.user_id == user_id).first()
    user_info = db.query(UserInfo).filter(UserInfo.user_id == user_id).first()
    illness_info = db.query(IllnessInfo).filter(IllnessInfo.user_id == user_id).first()
    feedback_context = get_recent_feedback_context(user_id)

    if not (sport_info and user_info and illness_info):
        raise HTTPException(status_code=404, detail="请先填写完整的健康信息")

    # 加载向量库与模型
    vectorstore = load_exercise_vectorstore()
    assert vectorstore is not None, "加载向量库失败"
    chain = get_sport_rag_chain(vectorstore)

    # 构造 Prompt
    prompt = f"""
    你是一位运动健康顾问，请根据以下用户的健康信息与运动反馈，从知识库中选择真实存在的运动，为用户生成一份个性化运动推荐（注意要有3种运动）。
    
    请确保：
    - 所有推荐运动必须来自知识库（知识库中每项运动的消耗卡路里量基于每10分钟的标准）
    - 根据每项运动单位时间消耗卡路里（每10分钟），合理估算运动时长（duration, 单位：分钟），使推荐运动总热量在 500 ~ 700 kcal 之间
    - 输出格式为标准 JSON 数组，每项包括以下字段：
    
    {{
      "exercise_name": "string",
      "duration": int
    }}
    
    【用户反馈】
    {feedback_context}
    
    【用户健康信息】
    性别: {user_info.gender}
    身高: {user_info.height} cm，体重: {user_info.weight} kg
    血压: {user_info.blood_pressure}，血糖: {user_info.blood_sugar}
    慢性病: {illness_info.chronic_diseases}
    过敏源: {illness_info.allergy_details}
    
    请直接输出标准 JSON，不要包含解释或代码块标记。
    示例如下：
    [
      {{
        "exercise_name": "慢跑",
        "duration": 30
      }},
      {{
        "exercise_name": "瑜伽",
        "duration": 20
      }},
      {{
        "exercise_name": "跳绳",
        "duration": 10
      }}
    ]

    """

    # 调用 RAG 模型
    response = chain.invoke({"query": prompt})
    result = response["result"]

    try:
        content = result.strip().replace("```json", "").replace("```", "").strip()
        items = json.loads(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"运动推荐返回格式错误：{e}")

    # 插入打卡记录
    all_results = []
    now = datetime.now()

    for item in items:
        exercise_name = item.get("exercise_name", "").strip()
        duration = item.get("duration", 0)

        if not exercise_name or duration <= 0:
            continue

        # 查找运动信息
        exercise = db.query(Exercise).filter(Exercise.exercise_name == exercise_name).first()
        if not exercise:
            continue

        calories_per_10min = exercise.calories_burn_rate or 0
        calories_burned = int(calories_per_10min * (duration / 10))

        checkin = ExerciseCheckin(
            user_id=user_id,
            checkin_date=None,
            exercise_id=exercise.exercise_id,
            duration=duration,
            exercise_name=exercise_name,
            calories_burned=calories_burned,
            additional_info=None,
            create_time=now,
            feedback=None
        )
        db.add(checkin)
        all_results.append({
            "exercise_name": exercise_name,
            "duration": duration,
            "calories_burned": calories_burned
        })

    db.commit()

    return {
        "message": "运动推荐生成成功",
        "recommendations": all_results
    }



if __name__ == "__main__":
    user_id = 2
    result = asyncio.run(generate_exercise_recommendation(user_id))
    print(result)