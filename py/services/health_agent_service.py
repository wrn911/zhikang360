from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_core.callbacks import AsyncCallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from huggingface_hub import snapshot_download
from langchain.schema import Document
import glob
import os
import asyncio
from typing import Dict, List, Any
import warnings

# 忽略特定的警告
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)


# 创建自定义回调类（用于接收流式 token）
class MyCallbackHandler(AsyncCallbackHandler):
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue

    async def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(token, end='')
        await self.queue.put(token)

    async def on_llm_end(self, *args, **kwargs) -> None:
        # 发送None作为结束信号
        await self.queue.put(None)


def get_embeddings():
    """获取嵌入模型"""
    model_path = snapshot_download(repo_id="BAAI/bge-small-zh-v1.5", repo_type="model")
    return HuggingFaceEmbeddings(
        model_name=model_path,
        model_kwargs={"device": "cuda:0"},
        encode_kwargs={"normalize_embeddings": True}
    )


def init_memory():
    """初始化对话记忆"""
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        input_key="input",
        output_key="output"
    )


def init_agent(
        model="glm-4-flash",
        api_key="118aea86606f4e2f82750c54d3bb380c.DxtxnaKQhFz5EHPY",
        base_url="https://open.bigmodel.cn/api/paas/v4/",
        callbacks=None,
        memory=None
):
    """初始化代理"""
    # 初始化 LLM
    llm = ChatOpenAI(
        model=model,
        base_url=base_url,
        api_key=api_key,
        streaming=True,
        callbacks=callbacks or [],
    )

    # 如果没有提供记忆实例，创建一个新的
    if memory is None:
        memory = init_memory()

    # 获取嵌入模型
    embeddings = get_embeddings()
    persist_directory = os.path.join(os.getcwd(), "vector_store")

    # 创建统一检索函数
    def unified_retriever(question_and_user_id):
        """统一检索全局知识库和用户知识库"""
        if isinstance(question_and_user_id, str):
            # 如果只传入问题，没有用户ID
            question = question_and_user_id
            user_id = None
        else:
            # 如果传入的是字典格式 {"question": "...", "user_id": ...}
            question = question_and_user_id.get("question", "")
            user_id = question_and_user_id.get("user_id")

        all_docs = []

        # 1. 检索全局知识库
        try:
            global_docsearch = Chroma(
                persist_directory=persist_directory,
                embedding_function=embeddings,
                collection_name="global_knowledge"
            )
            global_retriever = global_docsearch.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}
            )
            global_docs = global_retriever.get_relevant_documents(question)
            all_docs.extend(global_docs)
            print(f"全局知识库找到 {len(global_docs)} 个相关文档")
        except Exception as e:
            print(f"检索全局知识库时出错: {str(e)}")

        # 2. 检索用户知识库（如果有用户ID）
        if user_id:
            try:
                print(f"开始查询用户 {user_id} 的知识库")
                collection_name = f"user_{user_id}_knowledge"
                user_docsearch = Chroma(
                    persist_directory=persist_directory,
                    embedding_function=embeddings,
                    collection_name=collection_name
                )

                # 验证集合是否存在
                collection = user_docsearch._collection
                if collection and collection.count() > 0:
                    print(f"用户知识库集合存在，文档数量: {collection.count()}")
                    user_retriever = user_docsearch.as_retriever(
                        search_type="similarity",
                        search_kwargs={"k": 3}
                    )
                    user_docs = user_retriever.get_relevant_documents(question)
                    all_docs.extend(user_docs)
                    print(f"用户知识库找到 {len(user_docs)} 个相关文档")

                    # 在处理向量检索结果的地方添加
                    print("=== 检索到的文档内容 ===")
                    for i, doc in enumerate(user_docs):
                        print(f"文档 {i + 1}:")
                        print(f"来源: {doc.metadata.get('source', 'unknown')}")
                        print(f"类型: {doc.metadata.get('source_type', 'unknown')}")
                        print(f"内容: {doc.page_content[:200]}...")
                        print("-" * 50)
                else:
                    print(f"用户 {user_id} 的知识库为空或不存在")
            except Exception as e:
                print(f"查询用户知识库时出错: {str(e)}")

        # 返回合并后的文档内容
        if all_docs:
            combined_content = "\n\n".join([
                f"【文档{i + 1}】{doc.page_content}"
                for i, doc in enumerate(all_docs)
            ])
            print(f"总共找到 {len(all_docs)} 个相关文档，合并后内容长度: {len(combined_content)}")
            return combined_content
        else:
            print("未找到任何相关文档")
            return "暂无相关知识库内容"

    # 创建简化的提示模板
    template = """你是一个专业的AI助手。请基于以下知识库内容和对话历史来回答问题。
如果知识库中没有相关信息，请基于你的专业知识回答，但要说明这不是来自知识库的信息。

知识库内容:
{context}

对话历史:
{chat_history}

问题: {question}

回答:"""

    prompt = ChatPromptTemplate.from_template(template)

    # 使用LCEL创建链
    chain = (
            RunnableParallel({
                "context": unified_retriever,
                "question": RunnablePassthrough(),
                "chat_history": lambda _: memory.load_memory_variables({})["chat_history"]
            })
            | prompt
            | llm
            | StrOutputParser()
    )

    return chain


async def query_with_user_knowledge(chain, memory, question: str, user_id: int = None,
                                    callbacks: List[AsyncCallbackHandler] = None):
    """查询知识库，包括全局知识库和用户个人知识库"""

    # 准备输入数据，包含问题和用户ID
    input_data = {
        "question": question,
        "user_id": user_id
    }

    # 如果有回调函数，添加到配置中
    config = {}
    if callbacks:
        config["callbacks"] = callbacks

    print(f"开始查询，问题: {question}, 用户ID: {user_id}")

    # 调用链进行查询
    return await chain.ainvoke(input_data, config=config)