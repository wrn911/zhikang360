import os
from datetime import datetime
from http.client import HTTPException
from typing import List

from huggingface_hub import snapshot_download
from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from sqlalchemy.orm import Session
from models.database import UserFoodRecommendList, get_db
from models.database import FoodInfo
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI  # 或 deepseek模型封装的类
from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings


import re
from pypinyin import lazy_pinyin

def get_embeddings():
    """获取嵌入模型"""
    model_path = snapshot_download(repo_id="BAAI/bge-small-zh-v1.5", repo_type="model")
    return HuggingFaceEmbeddings(
        model_name=model_path,
        model_kwargs={"device": "cuda:0"},
        encode_kwargs={"normalize_embeddings": True}
    )

def clean_key(s):
    """将中文转拼音，去掉非法字符并确保符合 collection name 要求"""
    pinyin_str = "_".join(lazy_pinyin(s))
    # 替换所有非字母数字或下划线/横线为下划线
    pinyin_str = re.sub(r"[^a-zA-Z0-9_-]", "_", pinyin_str)
    # 替换连续多个下划线为一个
    pinyin_str = re.sub(r"_+", "_", pinyin_str)
    # 移除开头和结尾的下划线或横线
    pinyin_str = pinyin_str.strip("_-")
    return pinyin_str


def build_user_food_knowledge_by_category(user_id: int, db: Session):
    """为用户构建 27 类嵌入知识库，每类一个 collection"""
    records = db.query(UserFoodRecommendList).filter(
        UserFoodRecommendList.user_id == user_id
    ).all()

    if not records:
        print(f"用户 {user_id} 无推荐数据")
        return

    from langchain.schema import Document
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain.vectorstores import Chroma

    embeddings = get_embeddings()
    persist_dir = os.path.join(os.getcwd(), "vector_store", f"user_food_{user_id}")

    group_map = {}
    for r in records:
        raw_key = f"{r.aim}_{r.time}_{r.grocery}"
        key = clean_key(raw_key)  # 合法化
        if key not in group_map:
            group_map[key] = []
        content = f"{r.food_name}（权重 {r.weight:.2f}）大小是描述用户在{r.aim}的{r.time}{r.grocery}种类中对该食物的喜好程度。"
        group_map[key].append(Document(
            page_content=content,
            metadata={"food_id": r.food_id, "weight": r.weight}
        ))

    for key, docs in group_map.items():
        collection_name = f"user_{user_id}_food_{key}"
        # 防止过长截断
        collection_name = collection_name[:63]
        chroma = Chroma(
            embedding_function=embeddings,
            persist_directory=persist_dir,
            collection_name=collection_name
        )
        chroma.add_documents(docs)
        chroma.persist()
        print(f"✅ 嵌入完成: {collection_name}，共{len(docs)}条")


import shutil


def update_user_food_knowledge(user_id: int, db: Session):
    """更新用户知识库（删除 persist_dir 下所有向量集合）"""
    persist_dir = os.path.join(os.getcwd(), "vector_store", f"user_food_{user_id}")

    # 删除整个目录
    if os.path.exists(persist_dir):
        try:
            shutil.rmtree(persist_dir)
            print(f"✅ 已删除用户 {user_id} 的知识库目录：{persist_dir}")
        except Exception as e:
            print(f"❌ 删除目录失败：{e}")
    else:
        print(f"ℹ️ 知识库目录不存在：{persist_dir}")

    # 重新构建
    build_user_food_knowledge_by_category(user_id, db)


async def generate_three_meals_recommendation_r1(user_id: int, db: Session, model_chain):
    """使用 DeepSeek-R1 生成三餐推荐，每餐主食+正餐+辅食，写入 FoodRecommend 表"""
    from models.database import FoodInfo, UserInfo, IllnessInfo, FoodRecommend, Food, UserRecommendInfo, UserFoodRecommendList

    food_info = db.query(FoodInfo).filter(FoodInfo.user_id == user_id).first()
    user_info = db.query(UserInfo).filter(UserInfo.user_id == user_id).first()
    illness_info = db.query(IllnessInfo).filter(IllnessInfo.user_id == user_id).first()
    user_rec = db.query(UserRecommendInfo).filter(UserRecommendInfo.user_id == user_id).first()
    aim = food_info.aim or "正常"

    if not (food_info and user_info and illness_info and user_rec):
        raise HTTPException(status_code=404, detail="用户健康信息不完整")

    # 每餐热量目标
    total_kcal = user_rec.food_calories
    kcal_plan = {
        "早餐": int(total_kcal * 0.25),
        "午餐": int(total_kcal * 0.45),
        "晚餐": int(total_kcal * 0.30),
    }

    embeddings = get_embeddings()
    persist_dir = os.path.join(os.getcwd(), "vector_store", f"user_food_{user_id}")
    result_all = {}
    already_selected = set()

    for meal, kcal_target in kcal_plan.items():
        meal_result = []
        for grocery in ["主食", "正餐", "辅食"]:
            raw_key = f"{aim}_{meal}_{grocery}"
            key = clean_key(raw_key)
            collection = f"user_{user_id}_food_{key}"

            try:
                retriever = Chroma(
                    persist_directory=persist_dir,
                    embedding_function=embeddings,
                    collection_name=collection
                ).as_retriever(search_kwargs={"k": 1})
                docs = retriever.get_relevant_documents(f"{meal}的{grocery}")
                context = "\n".join([doc.page_content for doc in docs if doc.metadata.get("food_id") not in already_selected])
                if not context:
                    continue

                prompt = ChatPromptTemplate.from_template(
                    "你是营养推荐助手，请从以下食物中选出一个适合{aim}目标的{meal}{grocery}：\n\n{context}\n\n"
                    "只输出最合适的食物名（不附解释、不换行）"
                )

                food_name = model_chain.invoke(
                    prompt.format(aim=aim, meal=meal, grocery=grocery, context=context)
                ).strip()

                food_obj = db.query(Food).filter(Food.name == food_name).first()
                if not food_obj:
                    continue

                # 克数估算（默认按每100g估热量，逼近目标 kcal / 3）
                target_per_food_kcal = kcal_target / 3
                if not food_obj.calories:
                    gram_ate = 100
                else:
                    raw = (target_per_food_kcal * 100) / food_obj.calories
                    gram_ate = max(int(round(raw / 50) * 50), 50)

                def calc(n): return round((n or 0) * gram_ate / 100, 2)

                now = datetime.now()
                db.add(FoodRecommend(
                    user_id=user_id,
                    recommend_type=meal,
                    food_id=food_obj.id,
                    food_name=food_name,
                    gram_ate=gram_ate,
                    calories_ate=calc(food_obj.calories),
                    carbohydrates_ate=calc(food_obj.carbohydrates),
                    fat_ate=calc(food_obj.fat),
                    protein_ate=calc(food_obj.protein),
                    fiber_ate=calc(food_obj.fiber),
                    create_time=now
                ))

                already_selected.add(food_obj.id)
                meal_result.append({
                    "food_name": food_name,
                    "food_id": food_obj.id,
                    "gram_ate": gram_ate
                })

            except Exception as e:
                print(f"⚠️ {meal}-{grocery}推荐失败: {e}")
                continue

        result_all[meal] = meal_result

    db.commit()
    return {
        "message": "三餐推荐已生成（R1模型）",
        "recommendations": result_all
    }







