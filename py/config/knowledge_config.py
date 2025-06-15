import os
from typing import Dict, List


class KnowledgeConfig:
    """知识库配置管理"""

    # 文件和目录配置
    BASE_DIR = os.getcwd()
    VECTOR_STORE_DIR = os.path.join(BASE_DIR, "vector_store")
    UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
    USER_PROFILES_DIR = os.path.join(BASE_DIR, "user_profiles")
    GLOBAL_DATA_DIR = os.path.join(BASE_DIR, "data")
    TEMP_DIR = os.path.join(BASE_DIR, "temp_global")

    # 支持的文件类型
    SUPPORTED_EXTENSIONS = {'.txt', '.pdf', '.md', '.docx', '.csv'}
    SUPPORTED_MIME_TYPES = {
        'text/plain',
        'application/pdf',
        'text/markdown',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/csv',
        'application/octet-stream'  # 通用类型
    }

    # 文档处理配置
    TEXT_SPLITTER_CONFIG = {
        "chunk_size": 500,
        "chunk_overlap": 50,
        "separator": "\n"
    }

    # 向量数据库配置
    VECTOR_DB_CONFIG = {
        "collection_names": {
            "global": "global_knowledge",
            "user_prefix": "user_{user_id}_knowledge"
        },
        "embedding_model": {
            "repo_id": "BAAI/bge-small-zh-v1.5",
            "device": "cuda:0",
            "normalize_embeddings": True
        }
    }

    # 文件大小限制（字节）
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    MAX_CONTENT_LENGTH = 1024 * 1024  # 1MB for text content

    # 任务处理配置
    TASK_CONFIG = {
        "max_pending_tasks": 3,
        "max_retry_count": 3,
        "task_timeout": 300,  # 5分钟
        "background_scan_interval": 300  # 5分钟
    }

    # 日志配置
    LOGGING_CONFIG = {
        "level": "INFO",
        "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        "file_path": os.path.join(BASE_DIR, "logs", "knowledge.log")
    }

    @classmethod
    def get_user_collection_name(cls, user_id: int) -> str:
        """获取用户向量集合名称"""
        return cls.VECTOR_DB_CONFIG["collection_names"]["user_prefix"].format(user_id=user_id)

    @classmethod
    def get_global_collection_name(cls) -> str:
        """获取全局向量集合名称"""
        return cls.VECTOR_DB_CONFIG["collection_names"]["global"]

    @classmethod
    def is_supported_file_type(cls, filename: str) -> bool:
        """检查文件类型是否支持"""
        file_ext = os.path.splitext(filename)[1].lower()
        return file_ext in cls.SUPPORTED_EXTENSIONS

    @classmethod
    def is_supported_mime_type(cls, mime_type: str) -> bool:
        """检查MIME类型是否支持"""
        return mime_type in cls.SUPPORTED_MIME_TYPES

    @classmethod
    def ensure_directories(cls):
        """确保所有必要的目录存在"""
        directories = [
            cls.VECTOR_STORE_DIR,
            cls.UPLOAD_DIR,
            cls.USER_PROFILES_DIR,
            cls.GLOBAL_DATA_DIR,
            cls.TEMP_DIR,
            os.path.dirname(cls.LOGGING_CONFIG["file_path"])
        ]

        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

    @classmethod
    def get_file_size_limit_mb(cls) -> int:
        """获取文件大小限制（MB）"""
        return cls.MAX_FILE_SIZE // (1024 * 1024)

    @classmethod
    def validate_file_size(cls, file_size: int) -> bool:
        """验证文件大小是否在限制内"""
        return file_size <= cls.MAX_FILE_SIZE

    @classmethod
    def get_health_profile_filename(cls, user_id: int) -> str:
        """获取健康档案文件名"""
        return f"user_{user_id}_health_profile.txt"

    @classmethod
    def get_health_profile_path(cls, user_id: int) -> str:
        """获取健康档案完整路径"""
        filename = cls.get_health_profile_filename(user_id)
        return os.path.join(cls.USER_PROFILES_DIR, filename)


# 环境相关配置
class DevelopmentConfig(KnowledgeConfig):
    """开发环境配置"""
    TEXT_SPLITTER_CONFIG = {
        "chunk_size": 300,  # 开发环境使用较小的块
        "chunk_overlap": 30,
        "separator": "\n"
    }
    LOGGING_CONFIG = {
        **KnowledgeConfig.LOGGING_CONFIG,
        "level": "DEBUG"
    }


class ProductionConfig(KnowledgeConfig):
    """生产环境配置"""
    TEXT_SPLITTER_CONFIG = {
        "chunk_size": 800,  # 生产环境使用较大的块
        "chunk_overlap": 100,
        "separator": "\n"
    }
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 生产环境允许更大的文件
    TASK_CONFIG = {
        **KnowledgeConfig.TASK_CONFIG,
        "max_pending_tasks": 10,  # 生产环境处理更多并发任务
        "background_scan_interval": 120  # 更频繁的扫描
    }


# 根据环境变量选择配置
def get_config() -> KnowledgeConfig:
    """根据环境变量获取配置"""
    env = os.getenv('ENVIRONMENT', 'development').lower()

    if env == 'production':
        return ProductionConfig()
    else:
        return DevelopmentConfig()


# 全局配置实例
config = get_config()

# 在导入时确保目录存在
config.ensure_directories()