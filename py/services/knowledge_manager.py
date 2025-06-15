from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.database import UserKnowledgeFile, UserKnowledgeStatus
from services.file_loader import get_embeddings, MultiTypeDirectoryLoader, get_loader
from config.knowledge_config import config
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.schema import Document
from datetime import datetime
from typing import List, Optional, Dict, Any
import os
import json
import traceback
import glob
from utils.encryption import encrypt_content, decrypt_content


class KnowledgeManager:
    """统一的知识库管理服务，确保文件、数据库、向量库的一致性"""

    def __init__(self):
        self.embeddings = get_embeddings()
        self.persist_directory = config.VECTOR_STORE_DIR
        self.text_splitter = CharacterTextSplitter(**config.TEXT_SPLITTER_CONFIG)

    def get_user_collection(self, user_id: int):
        """获取用户的向量数据库集合"""
        collection_name = config.get_user_collection_name(user_id)
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name=collection_name
        )

    def get_global_collection(self):
        """获取全局知识库向量数据库集合"""
        collection_name = config.get_global_collection_name()
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name=collection_name
        )

    def load_global_knowledge(self, data_dir: str = None) -> Dict[str, Any]:
        """
        加载全局知识库

        Args:
            data_dir: 数据目录路径，默认使用配置中的全局数据目录

        Returns:
            Dict包含加载结果
        """
        try:
            print("开始加载全局知识库")

            # 确定数据目录
            if data_dir is None:
                data_dir = config.GLOBAL_DATA_DIR

            # 确保数据目录存在
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
                print(f"创建数据目录: {data_dir}")
                return {
                    "success": False,
                    "error": f"数据目录为空: {data_dir}",
                    "message": f"请在{data_dir}目录下放置支持的文件类型: {', '.join(config.SUPPORTED_EXTENSIONS)}"
                }

            # 检查目录中是否有支持的文件
            found_files = []
            for ext in config.SUPPORTED_EXTENSIONS:
                pattern = f"*{ext}"
                found_files.extend(glob.glob(os.path.join(data_dir, '**', pattern), recursive=True))

            if not found_files:
                return {
                    "success": False,
                    "error": "未找到支持的文件",
                    "message": f"请在{data_dir}目录下放置支持的文件类型: {', '.join(config.SUPPORTED_EXTENSIONS)}"
                }

            print(f"找到 {len(found_files)} 个支持的文件")

            # 使用自定义加载器加载文件
            loader = MultiTypeDirectoryLoader(data_dir)
            documents = loader.load()

            if not documents:
                return {
                    "success": False,
                    "error": "文档加载失败",
                    "message": "所有文件都无法成功加载"
                }

            print(f"成功加载了 {len(documents)} 个文档")

            # 为文档添加全局知识库标识
            for doc in documents:
                doc.metadata.update({
                    "source_type": "global_knowledge",
                    "load_time": datetime.now().isoformat()
                })

            # 切割文档
            split_docs = self.text_splitter.split_documents(documents)
            print(f"文档被分割成 {len(split_docs)} 个片段")

            # 清空现有的全局知识库并重新创建
            collection_name = config.get_global_collection_name()
            docsearch = Chroma.from_documents(
                documents=split_docs,
                embedding=self.embeddings,
                persist_directory=self.persist_directory,
                collection_name=collection_name
            )
            docsearch.persist()

            result = {
                "success": True,
                "documents_loaded": len(documents),
                "chunks_created": len(split_docs),
                "files_processed": len(found_files),
                "data_directory": data_dir
            }

            print(f"全局知识库加载完成: {result}")
            return result

        except Exception as e:
            print(f"加载全局知识库失败: {str(e)}")
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }

    def add_to_global_knowledge(self, file_path: str, file_name: str = None) -> Dict[str, Any]:
        """
        向全局知识库添加单个文件

        Args:
            file_path: 文件路径
            file_name: 文件名（可选）

        Returns:
            Dict包含添加结果
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")

            if file_name is None:
                file_name = os.path.basename(file_path)

            print(f"向全局知识库添加文件: {file_name}")

            # 加载单个文件
            loader = get_loader(file_path)
            documents = loader.load()

            if not documents:
                raise ValueError(f"文件加载失败或内容为空: {file_path}")

            # 添加元数据
            for doc in documents:
                doc.metadata.update({
                    "source": file_path,
                    "source_type": "global_knowledge",
                    "file_name": file_name,
                    "add_time": datetime.now().isoformat()
                })

            # 切割文档
            split_docs = self.text_splitter.split_documents(documents)

            # 添加到全局知识库
            docsearch = self.get_global_collection()
            vector_ids = docsearch.add_documents(documents=split_docs)
            docsearch.persist()

            result = {
                "success": True,
                "file_name": file_name,
                "chunks_added": len(split_docs),
                "vector_ids": vector_ids
            }

            print(f"文件添加到全局知识库成功: {result}")
            return result

        except Exception as e:
            print(f"添加文件到全局知识库失败: {str(e)}")
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }

    def clear_global_knowledge(self) -> Dict[str, Any]:
        """
        清空全局知识库

        Returns:
            Dict包含清空结果
        """
        try:
            print("开始清空全局知识库")

            # 删除向量数据库集合
            docsearch = self.get_global_collection()
            collection = docsearch._collection

            deleted_count = 0
            if collection:
                # 获取所有文档ID并删除
                all_docs = collection.get()
                if all_docs and all_docs.get('ids'):
                    deleted_count = len(all_docs['ids'])
                    collection.delete(ids=all_docs['ids'])
                    print(f"删除了 {deleted_count} 个向量")

            result = {
                "success": True,
                "deleted_count": deleted_count,
                "message": "全局知识库已清空"
            }

            print(f"全局知识库清空完成: {result}")
            return result

        except Exception as e:
            print(f"清空全局知识库失败: {str(e)}")
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }

    def get_global_knowledge_stats(self) -> Dict[str, Any]:
        """
        获取全局知识库统计信息

        Returns:
            Dict包含统计信息
        """
        try:
            docsearch = self.get_global_collection()
            collection = docsearch._collection

            if not collection:
                return {
                    "success": True,
                    "total_documents": 0,
                    "message": "全局知识库为空"
                }

            # 获取文档数量
            doc_count = collection.count()

            if doc_count == 0:
                return {
                    "success": True,
                    "total_documents": 0,
                    "message": "全局知识库为空"
                }

            # 获取文件类型统计
            all_docs = collection.get(include=["metadatas"])
            metadatas = all_docs.get("metadatas", [])

            file_types = {}
            sources = set()

            for metadata in metadatas:
                if metadata:
                    # 统计来源文件
                    source = metadata.get("source", "unknown")
                    sources.add(source)

                    # 统计文件类型
                    file_ext = os.path.splitext(source)[1].lower()
                    file_types[file_ext] = file_types.get(file_ext, 0) + 1

            result = {
                "success": True,
                "total_documents": doc_count,
                "unique_sources": len(sources),
                "file_types": file_types,
                "sources": list(sources)
            }

            return result

        except Exception as e:
            print(f"获取全局知识库统计信息失败: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def add_document(self, user_id: int, file_path: str, file_name: str,
                     file_type: str, source_type: str, content: str = None,
                     db: Session = None) -> Dict[str, Any]:
        """
        原子性地添加文档到所有存储

        Args:
            user_id: 用户ID
            file_path: 文件路径
            file_name: 文件名
            file_type: 文件类型
            source_type: 来源类型 (uploaded_file/health_profile)
            content: 文档内容（如果为None则从文件读取）
            db: 数据库会话

        Returns:
            Dict包含操作结果和文档信息
        """
        try:
            print(f"开始添加文档: 用户{user_id}, 文件{file_name}")

            # 1. 准备文档内容
            if content is None:
                # 判断是否为加密文件
                if file_path.endswith('.enc') and source_type in ["uploaded_file", "health_profile"]:
                    # 读取并解密
                    with open(file_path, 'r', encoding='utf-8') as f:
                        encrypted_content = f.read()
                    content = decrypt_content(encrypted_content, user_id)
                else:
                    # 普通文件直接读取
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

            if not content.strip():
                raise ValueError("文档内容为空")

            # 移除原来的加密逻辑，因为文件已经在上层加密了

            # 2. 创建文档对象和分割
            document = Document(
                page_content=content,  # 向量化使用明文
                metadata={
                    "source": file_path,
                    "source_type": source_type,
                    "user_id": user_id,
                    "file_name": file_name,
                    "update_time": datetime.now().isoformat()
                }
            )

            split_docs = self.text_splitter.split_documents([document])
            print(f"文档分割成 {len(split_docs)} 个片段")

            # 3. 添加到向量数据库并获取ID
            docsearch = self.get_user_collection(user_id)
            vector_ids = docsearch.add_documents(documents=split_docs)
            docsearch.persist()

            print(f"向量数据库添加完成，向量ID: {vector_ids}")

            # 4. 记录到关系数据库
            if db:
                file_size = len(content.encode('utf-8'))

                knowledge_file = UserKnowledgeFile(
                    user_id=user_id,
                    file_name=file_name,
                    file_path=file_path,
                    file_size=file_size,
                    file_type=file_type,
                    source_type=source_type,
                    status="active",
                    vector_ids=json.dumps(vector_ids) if vector_ids else None,
                    chunk_count=len(split_docs)
                )
                db.add(knowledge_file)
                db.flush()  # 获取ID但不提交

                result = {
                    "success": True,
                    "file_id": knowledge_file.id,
                    "vector_ids": vector_ids,
                    "chunk_count": len(split_docs),
                    "file_size": file_size
                }

                print(f"文档添加成功: {result}")
                return result
            else:
                return {
                    "success": True,
                    "vector_ids": vector_ids,
                    "chunk_count": len(split_docs)
                }

        except Exception as e:
            print(f"添加文档失败: {str(e)}")
            traceback.print_exc()

            # 清理已创建的向量（如果有的话）
            try:
                if 'vector_ids' in locals() and vector_ids:
                    docsearch = self.get_user_collection(user_id)
                    collection = docsearch._collection
                    if collection:
                        collection.delete(ids=vector_ids)
                        print(f"清理了失败的向量: {vector_ids}")
            except Exception as cleanup_error:
                print(f"清理向量时出错: {cleanup_error}")

            return {
                "success": False,
                "error": str(e)
            }

    def delete_document(self, user_id: int, file_id: int, db: Session) -> Dict[str, Any]:
        """
        原子性地从所有存储删除文档

        Args:
            user_id: 用户ID
            file_id: 文件ID
            db: 数据库会话

        Returns:
            Dict包含操作结果
        """
        try:
            print(f"开始删除文档: 用户{user_id}, 文件ID{file_id}")

            # 1. 获取文件记录
            file_record = db.query(UserKnowledgeFile).filter(
                and_(
                    UserKnowledgeFile.id == file_id,
                    UserKnowledgeFile.user_id == user_id,
                    UserKnowledgeFile.status == "active"
                )
            ).first()

            if not file_record:
                raise ValueError(f"文件记录不存在或已删除: {file_id}")

            # 2. 从向量数据库删除
            vector_ids_deleted = []
            if file_record.vector_ids:
                try:
                    vector_ids = json.loads(file_record.vector_ids)
                    docsearch = self.get_user_collection(user_id)
                    collection = docsearch._collection

                    if collection and vector_ids:
                        collection.delete(ids=vector_ids)
                        vector_ids_deleted = vector_ids
                        print(f"从向量库删除了 {len(vector_ids)} 个向量")
                except Exception as e:
                    print(f"删除向量时出错: {e}")
                    # 向量删除失败不应该阻止整个删除流程

            # 3. 删除物理文件（如果存在）
            file_deleted = False
            if file_record.file_path and os.path.exists(file_record.file_path):
                try:
                    os.remove(file_record.file_path)
                    file_deleted = True
                    print(f"删除物理文件: {file_record.file_path}")
                except Exception as e:
                    print(f"删除物理文件时出错: {e}")
                    # 物理文件删除失败不阻止数据库更新

            # 4. 更新数据库状态
            file_record.status = "deleted"
            if hasattr(file_record, 'updated_at'):
                file_record.updated_at = datetime.now()

            result = {
                "success": True,
                "file_id": file_id,
                "vector_ids_deleted": vector_ids_deleted,
                "file_deleted": file_deleted,
                "file_path": file_record.file_path
            }

            print(f"文档删除成功: {result}")
            return result

        except Exception as e:
            print(f"删除文档失败: {str(e)}")
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }

    def update_health_profile(self, user_id: int, profile_content: str,
                              db: Session) -> Dict[str, Any]:
        """
        原子性地更新用户健康档案

        Args:
            user_id: 用户ID
            profile_content: 健康档案内容
            db: 数据库会话

        Returns:
            Dict包含操作结果
        """
        try:
            print(f"开始更新用户 {user_id} 的健康档案")

            # 1. 准备新的健康档案文件路径
            new_file_path = config.get_health_profile_path(user_id)

            # 确保目录存在
            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

            # 2. 获取旧的健康档案记录
            old_health_files = db.query(UserKnowledgeFile).filter(
                and_(
                    UserKnowledgeFile.user_id == user_id,
                    UserKnowledgeFile.source_type == "health_profile",
                    UserKnowledgeFile.status == "active"
                )
            ).all()

            # 3. 先从向量数据库删除旧的健康档案向量
            old_file_paths_to_delete = []
            for old_file in old_health_files:
                # 删除向量
                if old_file.vector_ids:
                    try:
                        vector_ids = json.loads(old_file.vector_ids)
                        docsearch = self.get_user_collection(user_id)
                        collection = docsearch._collection
                        if collection and vector_ids:
                            collection.delete(ids=vector_ids)
                            print(f"删除旧健康档案向量: {len(vector_ids)} 个")
                    except Exception as e:
                        print(f"删除旧向量时出错: {e}")

                # 记录需要删除的旧文件路径（但排除与新文件路径相同的）
                if old_file.file_path and old_file.file_path != new_file_path:
                    old_file_paths_to_delete.append(old_file.file_path)

                # 标记为删除
                old_file.status = "deleted"
                if hasattr(old_file, 'updated_at'):
                    old_file.updated_at = datetime.now()

            # 4. 保存新的健康档案文件（加密存储）
            encrypted_content = encrypt_content(profile_content, user_id)
            with open(new_file_path + '.enc', 'w', encoding='utf-8') as f:
                f.write(encrypted_content)
            new_file_path = new_file_path + '.enc'
            print(f"加密健康档案已保存到: {new_file_path}")

            # 5. 添加新的健康档案到知识库
            new_filename = config.get_health_profile_filename(user_id)
            add_result = self.add_document(
                user_id=user_id,
                file_path=new_file_path,  # 传入加密文件路径
                file_name=new_filename,
                file_type="text/plain",
                source_type="health_profile",
                content=profile_content,  # 传入明文内容，避免重复解密
                db=db
            )

            if not add_result["success"]:
                raise Exception(f"添加新健康档案失败: {add_result.get('error')}")

            # 6. 更新用户知识库状态
            status_record = db.query(UserKnowledgeStatus).filter(
                UserKnowledgeStatus.user_id == user_id
            ).first()

            if status_record:
                status_record.health_profile_path = new_file_path
                status_record.last_knowledge_update = datetime.now()
                status_record.update_status = "idle"
                status_record.updated_at = datetime.now()
            else:
                status_record = UserKnowledgeStatus(
                    user_id=user_id,
                    health_profile_path=new_file_path,
                    last_knowledge_update=datetime.now(),
                    update_status="idle"
                )
                db.add(status_record)

            # 7. 提交数据库事务后再删除旧文件
            db.flush()  # 确保数据库操作成功

            # 删除旧的物理文件（排除新文件路径）
            for old_path in old_file_paths_to_delete:
                try:
                    if os.path.exists(old_path):
                        os.remove(old_path)
                        print(f"删除旧健康档案文件: {old_path}")
                except Exception as e:
                    print(f"删除旧文件时出错: {e}")

            result = {
                "success": True,
                "file_id": add_result["file_id"],
                "file_path": new_file_path,
                "chunk_count": add_result["chunk_count"],
                "old_files_deleted": len(old_health_files)
            }

            print(f"健康档案更新成功: {result}")
            return result

        except Exception as e:
            print(f"更新健康档案失败: {str(e)}")
            traceback.print_exc()

            # 清理可能创建的新文件（仅在确实失败时删除）
            try:
                if 'new_file_path' in locals() and os.path.exists(new_file_path):
                    # 检查是否真的需要清理（如果新文件路径与旧文件不同才清理）
                    should_cleanup = True
                    if 'old_health_files' in locals():
                        for old_file in old_health_files:
                            if old_file.file_path == new_file_path:
                                should_cleanup = False
                                break

                    if should_cleanup:
                        os.remove(new_file_path)
                        print(f"清理失败的新文件: {new_file_path}")
            except Exception as cleanup_error:
                print(f"清理新文件时出错: {cleanup_error}")

            return {
                "success": False,
                "error": str(e)
            }

    def sync_user_knowledge(self, user_id: int, db: Session) -> Dict[str, Any]:
        """
        同步用户知识库，检查并修复数据不一致问题

        Args:
            user_id: 用户ID
            db: 数据库会话

        Returns:
            Dict包含同步结果
        """
        try:
            print(f"开始同步用户 {user_id} 的知识库")

            # 获取数据库中的活跃文件记录
            active_files = db.query(UserKnowledgeFile).filter(
                and_(
                    UserKnowledgeFile.user_id == user_id,
                    UserKnowledgeFile.status == "active"
                )
            ).all()

            # 获取向量数据库中的所有文档
            docsearch = self.get_user_collection(user_id)
            collection = docsearch._collection

            vector_docs = []
            if collection and collection.count() > 0:
                # 获取所有向量文档的元数据
                all_docs = collection.get(include=["metadatas"])
                vector_docs = all_docs.get("metadatas", [])

            sync_result = {
                "db_files_count": len(active_files),
                "vector_docs_count": len(vector_docs),
                "issues_found": [],
                "actions_taken": []
            }

            # 检查文件是否存在但向量缺失
            for file_record in active_files:
                if file_record.vector_ids:
                    vector_ids = json.loads(file_record.vector_ids)
                    # 这里可以添加更详细的向量存在性检查
                else:
                    sync_result["issues_found"].append(f"文件 {file_record.id} 缺少向量ID")

                # 检查物理文件是否存在
                if file_record.file_path and not os.path.exists(file_record.file_path):
                    sync_result["issues_found"].append(f"物理文件不存在: {file_record.file_path}")

            print(f"知识库同步完成: {sync_result}")
            return sync_result

        except Exception as e:
            print(f"同步知识库失败: {str(e)}")
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }


# 全局实例
knowledge_manager = KnowledgeManager()