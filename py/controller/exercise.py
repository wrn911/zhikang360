import base64
from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter
from fastapi.responses import JSONResponse
import requests
import os

from services.food_services import call_glm4v
from services.food_services import get_food_docs_from_db, build_food_vectorstore, get_food_rag_chain, \
    load_food_vectorstore

router = APIRouter(prefix="/food", tags=["food"])

# 初始化食物向量知识库
# 如果向量库已存在则直接加载，否则从数据库构建
VECTORSTORE_DIR = "../vector_store/chroma_exercise"
if os.path.exists(VECTORSTORE_DIR) and os.listdir(VECTORSTORE_DIR):
    vectorstore = load_food_vectorstore(VECTORSTORE_DIR)  # 加载已有向量库
else:
    docs = get_food_docs_from_db()  # 从数据库获取食物数据
    vectorstore = build_food_vectorstore(docs, persist_dir=VECTORSTORE_DIR)  # 构建新向量库


@router.post("/update_vectorstore")
def update_vectorstore():
    """
    手动更新向量知识库API
    返回:
        dict: 包含操作结果的字典
    功能:
        1. 从数据库重新获取食物数据
        2. 重建向量知识库
    """
    from services.food_services import get_food_docs_from_db, build_food_vectorstore

    # 从数据库获取最新食物数据
    docs = get_food_docs_from_db()

    # 重建向量知识库
    build_food_vectorstore(docs, persist_dir=VECTORSTORE_DIR)

    return {"msg": "vectorstore updated"}