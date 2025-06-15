import base64
import json

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import requests
from huggingface_hub import snapshot_download
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# 配置GLM-4V模型参数
with open('../settings.json') as settings_file:
    glm_config = json.load(settings_file)['glm']
    GLM4V_API_KEY = glm_config['api_key']  # GLM-4V API密钥
    GLM4V_API_URL = glm_config['url']      # GLM-4V API地址
    GLM4V_MODEL = "glm-4v-flash"          # 使用的GLM-4V模型版本，可选"glm-4v-plus-0111"
def get_embeddings():
    """
    获取HuggingFace嵌入模型

    返回:
        HuggingFaceEmbeddings: 初始化好的嵌入模型实例
    """
    # 从HuggingFace Hub下载BAAI/bge-small-zh-v1.5嵌入模型
    model_path = snapshot_download(repo_id="BAAI/bge-small-zh-v1.5", repo_type="model")
    return HuggingFaceEmbeddings(
        model_name=model_path,  # 模型路径
        model_kwargs={"device": "cuda:0"},  # 使用GPU加速
        encode_kwargs={"normalize_embeddings": True}  # 归一化嵌入向量
    )


def get_exercise_docs_from_db(settings_path='../settings.json'):
    """
    从MySQL数据库读取运动消耗信息并生成文档

    参数:
        settings_path: 配置文件路径，默认为'settings.json'

    返回:
        list: 运动文档列表，每个元素包含运动名称和格式化内容
    """
    # 读取数据库配置
    with open(settings_path, encoding='utf-8') as settings_file:
        db = json.load(settings_file)['localdb']
        user = db['user']      # 数据库用户名
        password = db['password']  # 数据库密码
        host = db['host']      # 数据库主机
        port = db['port']      # 数据库端口
        database = db['database']  # 数据库名称

    # 创建数据库连接
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # 查询 exercise 表所有数据
        result = session.execute(text("SELECT * FROM exercise"))
        docs = []

        # 格式化每条运动记录为文本文档
        for row in result:
            doc = f"""运动名称：{row[1]}
                    类型：{row[2]}
                    消耗热量：{row[3]} 千卡/小时"""
            docs.append({"name": row[1], "content": doc})

        return docs
    finally:
        session.close()


def build_exercise_vectorstore(docs, persist_dir="./vector_store/chroma_exercise"):
    """
    构建运动消耗信息向量知识库

    参数:
        docs: 运动文档列表，来自 get_exercise_docs_from_db()
        persist_dir: 向量库持久化目录，默认为'./vector_store/chroma_exercise'

    返回:
        Chroma: 构建好的向量知识库实例
    """
    texts = [d["content"] for d in docs]
    metadatas = [{"name": d["name"]} for d in docs]

    embedding = get_embeddings()
    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=embedding,
        metadatas=metadatas,
        persist_directory=persist_dir
    )
    vectorstore.persist()
    return vectorstore


def load_exercise_vectorstore(persist_dir="./vector_store/chroma_exercise"):
    """
    加载已持久化的运动向量知识库

    参数:
        persist_dir: 向量库持久化目录

    返回:
        Chroma: 加载的向量知识库实例
    """
    embedding = get_embeddings()
    return Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding
    )

def get_sport_rag_chain(vectorstore):
    """
    构建食物营养RAG问答链

    参数:
        vectorstore: 食物向量知识库实例

    返回:
        RetrievalQA: 构建好的RAG问答链
    """
    # 配置检索器，返回最相关的3个文档
    retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

    # 定义问答提示模板
    prompt = ChatPromptTemplate.from_template(
        "请适当参考下列运动知识库内容，回答用户关于运动推荐的问题。\n"
        "⚠️ 请不要使用知识库中未出现的食物名称，否则视为无效推荐。\n"
        "知识库内容：\n{context}\n"
        "用户问题：{question}\n"
    )

    # 初始化GLM-4V大语言模型
    llm = ChatOpenAI(
        model=GLM4V_MODEL,  # 模型名称
        base_url=GLM4V_API_URL,  # API地址
        api_key=GLM4V_API_KEY  # API密钥
    )

    # 构建RAG问答链
    chain = RetrievalQA.from_chain_type(
        llm=llm,  # 语言模型
        retriever=retriever,  # 检索器
        chain_type="stuff",  # 链类型
        return_source_documents=True,  # 返回源文档
        chain_type_kwargs={"prompt": prompt}  # 提示模板
    )
    return chain


# ---------- 主程序 ----------
if __name__ == "__main__":
    print("开始构建exercise向量库...")
    docs = get_exercise_docs_from_db()
    vectorstore = build_exercise_vectorstore(docs)
    print("构建完成！\n")