from http.client import HTTPException
from sqlalchemy.orm import Session
from langchain.schema import Document
import os
from models.database import UserRecommendInfo, ExerciseCheckin, Exercise, UserExerciseRecommendList
from langchain.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate


def build_user_exercise_knowledge_by_category(user_id: int, db: Session):
    """为用户构建按运动类型分类的嵌入知识库，每类一个 collection"""

    records = db.query(UserExerciseRecommendList).filter(
        UserExerciseRecommendList.user_id == user_id
    ).all()

    if not records:
        print(f"用户 {user_id} 无运动推荐数据")
        return

    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
    persist_dir = os.path.join(os.getcwd(), "vector_store", f"user_exercise_{user_id}")

    group_map = {}
    for r in records:
        key = r.exercise_category.strip()  # e.g. 有氧运动、力量训练...
        if key not in group_map:
            group_map[key] = []
        content = f"{r.exercise_name}（权重 {r.weight:.2f}）的大小代表着{r.exercise_category}类中用户对运动的偏好。"
        group_map[key].append(Document(
            page_content=content,
            metadata={"exercise_id": r.exercise_id, "weight": r.weight}
        ))

    for category, docs in group_map.items():
        collection_name = f"user_{user_id}_exercise_{category}"
        Chroma.from_documents(
            docs,
            embedding=embeddings,
            collection_name=collection_name,
            persist_directory=persist_dir
        ).persist()
        print(f"✅ 嵌入完成: {collection_name}，共{len(docs)}条")



def update_user_exercise_knowledge(user_id: int, db: Session):
    """更新用户运动知识库（先删除所有类型 collection 再重建）"""

    persist_dir = os.path.join(os.getcwd(), "vector_store", f"user_exercise_{user_id}")
    embedding = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")

    # 枚举所有类别并尝试删除旧 collection
    categories = ["有氧运动", "力量训练", "球类运动", "游泳", "武术格斗"]
    for category in categories:
        collection = f"user_{user_id}_exercise_{category}"
        try:
            existing = Chroma(
                embedding_function=embedding,
                persist_directory=persist_dir,
                collection_name=collection
            )
            existing.delete_collection()
            print(f"✅ 已删除旧集合：{collection}")
        except Exception as e:
            print(f"⚠️ 删除集合 {collection} 失败或不存在：{e}")
    build_user_exercise_knowledge_by_category(user_id, db)


import random
from datetime import datetime

async def generate_three_exercise_recommendation_r1(user_id: int, db: Session, model_chain):

    # 1. 获取用户推荐目标
    user_rec = db.query(UserRecommendInfo).filter(UserRecommendInfo.user_id == user_id).first()
    if not user_rec or not user_rec.exercise_calories:
        raise HTTPException(status_code=404, detail="用户运动推荐信息缺失")

    total_kcal = user_rec.exercise_calories
    plan = {
        "有氧运动": int(total_kcal * 0.5),
        "力量训练": int(total_kcal * 0.2),
    }

    # 在 ["球类运动", "游泳", "武术格斗"] 中随机一个作为“其他”
    optional_category = random.choice(["球类运动", "游泳", "武术格斗"])
    plan[optional_category] = total_kcal - plan["有氧运动"] - plan["力量训练"]

    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
    persist_dir = os.path.join(os.getcwd(), "vector_store", f"user_exercise_{user_id}")
    already_selected = set()
    result = []

    for category, kcal_target in plan.items():
        collection_name = f"user_{user_id}_exercise_{category}"
        try:
            retriever = Chroma(
                persist_directory=persist_dir,
                embedding_function=embeddings,
                collection_name=collection_name
            ).as_retriever(search_kwargs={"k": 5})

            docs = retriever.get_relevant_documents(f"{category}推荐")
            context = "\n".join([
                doc.page_content for doc in docs
                if doc.metadata.get("exercise_id") not in already_selected
            ])
            if not context:
                continue

            prompt = ChatPromptTemplate.from_template(
                "你是运动推荐助手，请从以下运动中选出一个适合用户的{category}：\n\n{context}\n\n"
                "只输出最合适的运动名称（不附解释、不换行）"
            )
            exercise_name = model_chain.invoke(
                prompt.format(category=category)
            ).strip()

            exercise_obj = db.query(Exercise).filter(Exercise.exercise_name == exercise_name).first()
            if not exercise_obj or not exercise_obj.calories_burn_rate:
                continue

            # 计算时长：calories_burn_rate 是每 10 分钟消耗
            burn_per_10min = float(exercise_obj.calories_burn_rate)
            duration = int(round((kcal_target / burn_per_10min) * 10))
            duration = max((duration // 5) * 5, 5)  # 向下取整为 5 的倍数

            calories_burned = int(round(burn_per_10min * duration / 10))

            db.add(ExerciseCheckin(
                user_id=user_id,
                exercise_id=exercise_obj.exercise_id,
                exercise_name=exercise_obj.exercise_name,
                duration=duration,
                calories_burned=calories_burned,
                create_time=datetime.now()
            ))

            already_selected.add(exercise_obj.exercise_id)
            result.append({
                "category": category,
                "exercise_id": exercise_obj.exercise_id,
                "exercise_name": exercise_obj.exercise_name,
                "duration": duration,
                "calories_burned": calories_burned
            })

        except Exception as e:
            print(f"⚠️ 推荐失败 [{category}]: {e}")
            continue

    db.commit()
    return {
        "message": "三项运动推荐已生成（R1模型）",
        "recommendations": result
    }
