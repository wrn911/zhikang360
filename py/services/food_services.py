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
with open('settings.json') as settings_file:
    glm_config = json.load(settings_file)['glm']
    GLM4V_API_KEY = glm_config['api_key']  # GLM-4V API密钥
    GLM4V_API_URL = glm_config['url']      # GLM-4V API地址
    GLM4V_MODEL = "glm-4v-flash"          # 使用的GLM-4V模型版本，可选"glm-4v-plus-0111"

def call_glm4v(image_base64: str, distance_cm: int = 30):
    """
    调用GLM-4V模型识别食物图片
    
    参数:
        image_base64: 图片的base64编码字符串
        distance_cm: 摄像头与食物的距离(厘米)，默认为30
        
    返回:
        str: 模型返回的JSON格式字符串，包含食物名称和重量
        
    异常:
        HTTPException: 模型调用失败或返回格式异常时抛出
    """
    # 构造识别prompt，指定输出格式和要求
    prompt = (
        f"请识别图片中所有食物的种类和重量，单位为克。"
        f"摄像头与食物的距离为{distance_cm}厘米。"
        f"如果有多个食物，请分别列出。"
        f"返回格式为JSON数组，每个元素包含name和weight字段。"
    )
    
    # 设置API请求头
    headers = {
        "Authorization": f"Bearer {GLM4V_API_KEY}",  # API认证
        "Content-Type": "application/json"          # 内容类型
    }
    
    # 构造请求体
    payload = {
        "model": GLM4V_MODEL,  # 模型名称
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": image_base64}  # 图片URL
                    },
                    {
                        "type": "text",
                        "text": prompt  # 识别指令
                    }
                ]
            }
        ]
    }
    
    # 调用GLM-4V API
    resp = requests.post(
        GLM4V_API_URL+"/chat/completions", 
        headers=headers, 
        json=payload, 
        timeout=60  # 超时60秒
    )
    
    # 检查响应状态码
    if resp.status_code != 200:
        raise HTTPException(
            status_code=500, 
            detail=f"模型调用失败: {resp.text}"
        )
    
    # 解析模型返回结果
    data = resp.json()
    try:
        result = data["choices"][0]["message"]["content"]
        # 去除返回结果中的Markdown标记
        result = result.replace("```json", "").replace("```", "").strip()
        return result
    except Exception:
        raise HTTPException(
            status_code=500, 
            detail=f"模型返回格式异常: {data}"
        )


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


def get_food_docs_from_db(settings_path='settings.json'):
    """
    从MySQL数据库读取食物营养信息并生成文档

    参数:
        settings_path: 配置文件路径，默认为'settings.json'

    返回:
        list: 食物文档列表，每个元素包含食物名称和格式化内容
    """
    # 读取数据库配置
    with open(settings_path, encoding='utf-8') as settings_file:
        db = json.load(settings_file)['localdb']
        user = db['user']  # 数据库用户名
        password = db['password']  # 数据库密码
        host = db['host']  # 数据库主机
        port = db['port']  # 数据库端口
        database = db['database']  # 数据库名称

    # 创建数据库连接
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # 查询food表所有数据
        result = session.execute(text("SELECT * FROM food"))
        docs = []

        # 格式化每条食物记录
        for row in result:
            doc = f"""食物名称：{row[1]}
                    类别：{row[2]}
                    热量：{row[3]} 千卡
                    碳水化合物：{row[4]} 克
                    脂肪：{row[5]} 克
                    蛋白质：{row[6]} 克
                    纤维素：{row[7]} 克
                    单位：{row[8]}"""
            docs.append({"name": row[1], "content": doc})

        return docs
    finally:
        # 确保会话关闭
        session.close()


def build_food_vectorstore(docs, persist_dir="./vector_store/chroma_food"):
    """
    构建食物营养向量知识库

    参数:
        docs: 食物文档列表，来自get_food_docs_from_db()
        persist_dir: 向量库持久化目录，默认为'../vector_store/chroma_food'

    返回:
        Chroma: 构建好的向量知识库实例
    """
    # 提取文档内容和元数据
    texts = [d["content"] for d in docs]  # 食物营养文本内容
    metadatas = [{"name": d["name"]} for d in docs]  # 食物名称作为元数据

    # 获取嵌入模型并构建向量库
    embedding = get_embeddings()
    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=embedding,
        metadatas=metadatas,
        persist_directory=persist_dir
    )

    # 持久化向量库
    vectorstore.persist()
    return vectorstore


def load_food_vectorstore(persist_dir="./vector_store/chroma_food"):
    """
    加载已持久化的食物向量知识库

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


def get_food_rag_chain(vectorstore):
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
        "请适当参考下列食物知识库内容，回答用户关于食物推荐的问题。\n"
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