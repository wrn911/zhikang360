from langchain.text_splitter import CharacterTextSplitter
from langchain_core.callbacks import AsyncCallbackHandler
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

import os
from langchain.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader,
    UnstructuredMarkdownLoader,
    UnstructuredWordDocumentLoader,
    CSVLoader,
    JSONLoader,
)


def get_loader(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.txt':
        return TextLoader(file_path, encoding='utf-8')
    elif ext == '.pdf':
        return PyPDFLoader(file_path)
    elif ext == '.md':
        return UnstructuredMarkdownLoader(file_path)
    elif ext == '.docx':
        return UnstructuredWordDocumentLoader(file_path)
    elif ext == '.csv':
        return CSVLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


class MultiTypeDirectoryLoader:
    """支持中文文件名，兼容多类型文档加载器"""

    def __init__(self, path: str):
        self.path = path

    def load(self) -> List[Document]:
        all_docs = []
        for root, _, files in os.walk(self.path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    loader = get_loader(file_path)
                    docs = loader.load()
                    all_docs.extend(docs)
                except ValueError as e:
                    print(f"⚠️ 跳过不支持的文件类型: {file_path} ({e})")
                except Exception as e:
                    print(f"❌ 加载失败: {file_path} ({e})")
        if not all_docs:
            print("⚠️ 没有找到任何支持的文档文件。请确保在目标目录下有 .txt 或 .pdf 等支持的文件。")
        return all_docs


def get_embeddings():
    """获取嵌入模型"""
    model_path = snapshot_download(repo_id="BAAI/bge-small-zh-v1.5", repo_type="model")
    return HuggingFaceEmbeddings(
        model_name=model_path,
        model_kwargs={"device": "cuda:0"},
        encode_kwargs={"normalize_embeddings": True}
    )


def load_global_knowledge():
    """加载全局知识库"""
    embeddings = get_embeddings()
    persist_directory = os.path.join(os.getcwd(), "vector_store")

    # 确保数据目录存在
    data_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"创建数据目录: {data_dir}")

    # 使用自定义加载器加载文件
    loader = MultiTypeDirectoryLoader(data_dir)
    try:
        documents = loader.load()
        print(f"成功加载了 {len(documents)} 个文档")

        if not documents:
            print("警告: 没有找到任何支持的文档文件。请确保在data目录下放置.txt或.pdf文件。")
            return None

        # 初始化文本分割器
        text_splitter = CharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separator="\n"
        )

        # 切割加载的 document
        split_docs = text_splitter.split_documents(documents)
        print(f"文档被分割成 {len(split_docs)} 个片段")

        # 创建全局知识库集合
        docsearch = Chroma.from_documents(
            documents=split_docs,
            embedding=embeddings,
            persist_directory=persist_directory,
            collection_name="global_knowledge"
        )
        docsearch.persist()
        print(f"全局知识库已成功索引并保存到: {persist_directory}")

    except Exception as e:
        print(f"加载文档时出错: {str(e)}")
        return None

