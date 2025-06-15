import os
import re
import json
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from huggingface_hub import snapshot_download
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA


# ===== 1. 嵌入模型 =====
def get_embeddings():
    model_path = snapshot_download(repo_id="BAAI/bge-small-zh-v1.5", repo_type="model")
    return HuggingFaceEmbeddings(
        model_name=model_path,
        model_kwargs={"device": "cuda:0"},
        encode_kwargs={"normalize_embeddings": True}
    )


# ===== 2. 数据库会话 =====
def get_session(settings_path="../settings.json"):
    with open(settings_path, encoding='utf-8') as f:
        db = json.load(f)['localdb']
    url = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    return Session()


# ===== 3. 获取用户列表 =====
def get_all_user_ids(session):
    result = session.execute(text("SELECT id FROM user"))
    return [row[0] for row in result]


# ===== 4. 获取指定用户所有反馈并格式化 =====
def get_user_feedback_docs(session, user_id):
    result = session.execute(text(f"""
        SELECT content_food, content_sport, content_sleep, publish_time 
        FROM feedback WHERE user_id = {user_id}
    """))

    docs = []
    for i, row in enumerate(result):
        food, sport, sleep = row[0] or "", row[1] or "", row[2] or ""
        publish_time = str(row[3]) if row[3] else "未知时间"
        text_block = (
            f"反馈时间：{publish_time}\n"
            f"饮食反馈：{food}\n"
            f"运动反馈：{sport}\n"
            f"睡眠反馈：{sleep}"
        ).strip()
        docs.append({
            "name": f"user_{user_id}_fb_{i}",
            "content": text_block,
            "date": publish_time
        })
    return docs


# ===== 5. 构建向量库 =====
def build_user_vectorstore(user_id, docs, persist_dir_root="./vector_store"):
    if not docs:
        print(f"⚠️ 用户 {user_id} 无反馈内容，跳过构建向量库")
        return None  # 或 return 空 vectorstore
    persist_dir = os.path.join(persist_dir_root, f"feedback_{user_id}")
    texts = [d["content"] for d in docs]
    metadatas = [{"name": d["name"], "date": d["date"]} for d in docs]

    embedding = get_embeddings()
    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=embedding,
        metadatas=metadatas,
        persist_directory=persist_dir
    )
    vectorstore.persist()
    print(f"✅ 用户 {user_id} 向量库构建完成，共 {len(docs)} 条反馈")
    return vectorstore

# ===== 6. 向现有向量库追加新文档 =====
def update_user_vectorstore(user_id, new_docs, persist_dir_root="./vector_store"):
    if not new_docs:
        print(f"⚠️ 用户 {user_id} 更新内容为空，跳过更新")
        return

    persist_dir = os.path.join(persist_dir_root, f"feedback_{user_id}")
    embedding = get_embeddings()

    if os.path.exists(persist_dir):
        vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embedding)

        # 获取现有文档内容，用于去重
        existing_docs = vectorstore.get()["documents"]
        existing_texts_set = set(existing_docs)

        # 筛选去重后的新文档
        unique_docs = [d for d in new_docs if d["content"] not in existing_texts_set]

        if not unique_docs:
            print(f"ℹ️ 用户 {user_id} 的新内容已全部存在，跳过追加")
            return

        texts = [d["content"] for d in unique_docs]
        metadatas = [{"name": d["name"], "date": d["date"]} for d in unique_docs]
        vectorstore.add_texts(texts, metadatas)
        vectorstore.persist()
        print(f"🆕 用户 {user_id} 向量库已更新（新增 {len(unique_docs)} 条）")

    else:
        print(f"⚠️ 向量库不存在，为用户 {user_id} 新建向量库")
        build_user_vectorstore(user_id, new_docs, persist_dir_root)



# ===== 7. 加载用户向量库 =====
def load_user_vectorstore(user_id, persist_dir_root="./vector_store"):
    persist_dir = os.path.join(persist_dir_root, f"feedback_{user_id}")
    embedding = get_embeddings()
    return Chroma(persist_directory=persist_dir, embedding_function=embedding)


# ===== 8. 提取问题中的时间线索 =====
def extract_time_filter(question: str):
    question = question.lower()
    now = datetime.now()
    if "最近" in question or "最新" in question:
        return now - timedelta(days=7)
    match = re.search(r"(\d{4})[-年](\d{1,2})", question)
    if match:
        return datetime(int(match.group(1)), int(match.group(2)), 1)
    match = re.search(r"(\d{1,2})月", question)
    if match:
        return datetime(now.year, int(match.group(1)), 1)
    return None


# ===== 9. 查询用户反馈（含时间过滤） =====
def query_user_feedback(user_id: int, question: str):
    print(f"\n🔍 查询用户{user_id}反馈：{question}")
    vectorstore = load_user_vectorstore(user_id)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    docs = retriever.get_relevant_documents(question)

    # 过滤时间
    time_threshold = extract_time_filter(question)
    if time_threshold:
        print(f"🕒 仅保留时间 >= {time_threshold.date()} 的反馈")
        docs = [
            doc for doc in docs
            if "date" in doc.metadata and str(doc.metadata["date"]) >= str(time_threshold.date())
        ]

    # 构建 QA 模板
    prompt = ChatPromptTemplate.from_template(
        "你是一位健康反馈分析师。以下是用户过往的健康反馈记录：\n"
        "{context}\n\n"
        "请基于上述内容，回答用户的问题：{question}\n"
        "不要编造反馈数据库中不存在的信息。"
    )

    llm = ChatOpenAI(temperature=0)
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=lambda _: docs,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )

    response = chain.run(question=question)
    print("💬 回答：", response)
    return response


# ===== 10. 主程序（构建所有用户） =====
if __name__ == "__main__":
    print("开始为所有用户构建反馈向量库...")
    session = get_session()
    user_ids = get_all_user_ids(session)

    for user_id in user_ids:
        docs = get_user_feedback_docs(session, user_id)
        build_user_vectorstore(user_id, docs)

    session.close()
    print("✅ 所有用户处理完成！")

    # 测试查询
    query_user_feedback(user_id=2, question="请总结该用户最近的睡眠反馈")
    query_user_feedback(user_id=2, question="该用户在5月有哪些运动建议？")
