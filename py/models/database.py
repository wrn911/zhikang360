import json

from sqlalchemy import create_engine, Column, DECIMAL, Integer, String, Double, DateTime, ForeignKey, Boolean, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# 数据库连接配置
with open('settings.json') as settings_file:
    db = json.load(settings_file)['localdb']
    user = db['user']
    password = db['password']
    host = db['host']
    port = db['port']
    database = db['database']
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

# 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    username = Column(String(255), nullable=True, comment="用户名")
    password = Column(String(255), nullable=True, comment="密码")
    name = Column(String(255), nullable=True, comment="姓名")
    avatar = Column(String(255), nullable=True, comment="头像")
    role = Column(String(255), nullable=True, comment="角色标识")
    phone = Column(String(255), nullable=True, comment="电话")
    email = Column(String(255), nullable=True, comment="邮箱")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username = Column(String(255), nullable=False, unique=True, comment="账号（唯一）")
    password = Column(String(512), nullable=False, comment="密码")
    avatar = Column(String(512), nullable=True, comment="头像URL")
    phone = Column(String(20), nullable=True, unique=True, comment="电话（唯一）")
    if_new = Column(Boolean, nullable=False, default=True, comment="是否新用户（0否 1是）")
    register_time = Column(DateTime, nullable=False, default=datetime.now, comment="注册时间")
    last_time = Column(DateTime, nullable=True, comment="最后登录时间")
    role = Column(String(255), nullable=True, comment="用户标识")

    # 关联聊天历史
    chat_histories = relationship("ChatHistory", back_populates="user")
    # 关联会话历史
    chat_sessions = relationship("ChatSession", back_populates="user")
    # 关联用户知识库文件
    knowledge_files = relationship("UserKnowledgeFile", back_populates="user")


class ChatHistory(Base):
    __tablename__ = "chat_histories"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, comment="用户ID")
    question = Column(String(1000), nullable=False, comment="问题")
    answer = Column(String(4000), nullable=False, comment="回答")
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=True, comment="会话ID")

    # 关联用户
    user = relationship("User", back_populates="chat_histories")
    # 关联会话
    session = relationship("ChatSession", back_populates="chat_histories")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="会话ID")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, comment="用户ID")
    title = Column(String(255), nullable=False, comment="会话标题")
    agent_id = Column(String(50), default="general", nullable=False)  # 新增这一行
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关联用户
    user = relationship("User", back_populates="chat_sessions")
    # 关联聊天历史
    chat_histories = relationship("ChatHistory", back_populates="session")


class UserKnowledgeFile(Base):
    __tablename__ = "user_knowledge_files"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="文件ID")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, comment="用户ID")
    file_name = Column(String(255), nullable=False, comment="文件名")
    file_path = Column(String(512), nullable=False, comment="文件路径")
    file_size = Column(Integer, nullable=False, comment="文件大小")
    file_type = Column(String(50), nullable=False, comment="文件类型")
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")  # 新增
    status = Column(String(20), nullable=False, default="active", comment="文件状态")
    source_type = Column(String(20), default="uploaded_file", comment="来源类型(uploaded_file/health_profile)")

    # 新增字段 - 用于关联向量数据库
    vector_ids = Column(String(2000), nullable=True, comment="向量数据库中对应的文档ID列表（JSON格式）")
    chunk_count = Column(Integer, nullable=True, comment="分割后的片段数量")

    # 关联用户
    user = relationship("User", back_populates="knowledge_files")

class FoodInfo(Base):
    __tablename__ = "food_info"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, comment="user_id对应")
    aim = Column(String(1000), comment="饮食目标")
    preferences = Column(String(1000), comment="饮食偏好（顿号分隔存储，如：素食、低糖）")
    avoids = Column(String(1000), comment="忌口食物（顿号分隔存储，如：海鲜、花生）")
    willingness = Column(String(1000), comment="饮食计划配合意愿")
    create_time = Column(DateTime, default=datetime.now, comment="记录创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="记录更新时间")


class UserInfo(Base):
    __tablename__ = "user_basic_info"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True, comment="user id")
    gender = Column(String(10), nullable=False, comment="性别")
    birth_date = Column(DateTime, comment="出生日期")
    height = Column(DECIMAL(5, 1), comment="身高")
    weight = Column(DECIMAL(5, 1), comment="体重")
    blood_pressure = Column(String(20), comment="血压")
    blood_sugar = Column(DECIMAL(5, 1), comment="血糖")
    update_time_h = Column(DateTime, comment="身高体重更新时间")
    update_time_w = Column(DateTime, comment="体重更新时间")
    update_time_bp = Column(DateTime, comment="血压更新时间")
    update_time_bs = Column(DateTime, comment="血糖更新时间")

class SleepInfo(Base):
    __tablename__ = "sleep_info"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, comment="关联用户ID")
    sleep_time = Column(String(255), comment="睡眠时间（格式: HH:mm, 如 23:30）")
    wakeup_time = Column(String(255), comment="起床时间（格式: HH:mm, 如 07:00）")
    emotions = Column(String(255), comment="情绪选择（顿号分隔，如：平静、焦虑、愉悦）")
    create_time = Column(DateTime, default=datetime.now, comment="记录创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="记录更新时间")

class SportInfo(Base):
    __tablename__ = "sport_info"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, comment="user_id对应")
    preferences = Column(String(1000), comment="运动偏好")
    weaknesses = Column(String(1000), comment="对厌的运动")
    experience = Column(String(1000), comment="健身经历")
    intensity = Column(String(1000), comment="运动强度偏好")
    willingness = Column(String(1000), comment="运动计划配合意愿")
    free_times = Column(String(1000), comment="空闲时间")
    create_time = Column(DateTime, default=datetime.now, comment="记录创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="记录更新时间")

class IllnessInfo(Base):
    __tablename__ = "illness_info"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, comment="关联用户ID")
    allergy_type = Column(String(200), comment="过敏类型")
    allergy_details = Column(String(500), comment="过敏详情（顿号分隔，如：海鲜、花生）")
    chronic_diseases = Column(String(500), comment="慢性病（顿号分隔，如：高血压、糖尿病）")
    health_issues = Column(String(1000), comment="其他健康问题（自由文本描述）")
    create_time = Column(DateTime, default=datetime.now, comment="记录创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="记录更新时间")

class FoodRecommend(Base):
    __tablename__ = "food_recommend"

    recommend_id = Column(Integer, primary_key=True, autoincrement=True, comment="推荐记录ID")
    user_id = Column(Integer, nullable=False, comment="用户ID")
    recommend_type = Column(String(20), nullable=False, comment="推荐类型(早餐/午餐/晚餐)")
    food_id = Column(Integer, nullable=False, comment="食物ID")
    food_name = Column(String(100), nullable=False, comment="食物名称")
    gram_ate = Column(Integer, nullable=False, comment="摄入克数")
    calories_ate = Column(Double, nullable=False, comment="摄入卡路里")
    carbohydrates_ate = Column(Double, nullable=False, comment="摄入碳水")
    fat_ate = Column(Double, nullable=False, comment="摄入脂肪")
    protein_ate = Column(Double, nullable=False, comment="摄入蛋白质")
    fiber_ate = Column(Double, nullable=False, comment="摄入纤维素")
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")

class ExerciseCheckin(Base):
    __tablename__ = "exercise_checkin"

    checkin_id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    user_id = Column(Integer, nullable=False, comment="外键关联 user_account(user_id)")
    checkin_date = Column(DateTime, nullable=True, comment="打卡时间")
    exercise_id = Column(Integer, nullable=True, comment="运动类型（或关联运动表的 exercise_id）")
    duration = Column(Integer, nullable=True, comment="运动时长（分钟）")
    exercise_name = Column(String(255), nullable=True, comment="运动名称")
    calories_burned = Column(Integer, nullable=True, comment="消耗卡路里")
    additional_info = Column(String(255), nullable=True, comment="附加信息（如步数，组数，次数等）")
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")
    feedback = Column(Integer, nullable=True, comment="用户反馈：0~2，从轻松到疲惫")

class Food(Base):
    __tablename__ = 'food'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, comment='食物名称')
    category = Column(String(255), comment='食物种类')
    calories = Column(Integer, comment='卡路里')
    carbohydrates = Column(Double, comment='碳水化合物')
    fat = Column(Double, comment='脂肪')
    protein = Column(Double, comment='蛋白质')
    fiber = Column(Double, comment='纤维素')
    unit = Column(String(255), comment='度量单位')  # 如：100g、1盘、1碗等

class UserRecommendInfo(Base):
    __tablename__ = 'user_recommend_info'

    user_id = Column(Integer, primary_key=True)
    food_calories = Column(Integer)
    exercise_calories = Column(Integer)
    sleep_time_start = Column(Time)
    sleep_time_end = Column(Time)

class Exercise(Base):
    __tablename__ = "exercise"

    exercise_id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    exercise_name = Column(String(100), nullable=False, comment="运动名称")
    exercise_category = Column(String(50), nullable=True, comment="运动类别")
    calories_burn_rate = Column(Integer, nullable=True, comment="单位时间消耗卡路里")

class Music(Base):
    __tablename__ = 'music'

    music_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    duration = Column(Integer, nullable=False)
    music_url = Column(String(255), nullable=False)
    play_count = Column(Integer, default=0)  # 默认播放次数为0
    create_time = Column(DateTime, default=datetime.now)  # 自动填充创建时间
    if_favorite = Column(Boolean, default=False)  # 默认未收藏

class FoodCheckin(Base):
    __tablename__ = "food_checkin"

    checkin_id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    user_id = Column(Integer, nullable=False, comment="外键关联 user_account(user_id)")
    checkin_type = Column(String(255), comment="餐别（早午晚餐）")
    food_id = Column(Integer, nullable=False, comment="关联食物表的id）")
    food_name = Column(String(255), nullable=False, comment="食物名称")
    gram_ate = Column(Integer, comment="摄入克数")
    calories_ate = Column(Double, comment="摄入卡路里")
    carbohydrates_ate = Column(Double, comment="摄入碳水")
    fat_ate = Column(Double, comment="摄入脂肪")
    protein_ate = Column(Double, comment="摄入蛋白质")
    fiber_ate = Column(Double, comment="摄入纤维素")
    create_time = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")

class UserKnowledgeStatus(Base):
    __tablename__ = "user_knowledge_status"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True, comment="用户ID")
    health_profile_path = Column(String(512), comment="健康档案文件路径")
    last_health_update = Column(DateTime, comment="最后健康数据更新时间")
    last_knowledge_update = Column(DateTime, comment="最后知识库更新时间")
    update_status = Column(String(20), default="idle", comment="更新状态(idle/pending/updating)")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关联用户
    user = relationship("User", backref="knowledge_status")


class KnowledgeUpdateTask(Base):
    __tablename__ = "knowledge_update_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, comment="用户ID")
    task_type = Column(String(50), default="health_data_sync", comment="任务类型")
    status = Column(String(20), default="pending", comment="任务状态(pending/processing/completed/failed)")
    retry_count = Column(Integer, default=0, comment="重试次数")
    error_message = Column(String(1000), comment="错误信息")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    processed_at = Column(DateTime, comment="处理时间")

    # 关联用户
    user = relationship("User", backref="update_tasks")

class UserFoodRecommendList(Base):
    __tablename__ = 'user_food_recommend_list'

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    user_id = Column(Integer, nullable=False, comment="用户ID")
    food_recommend_list_id = Column(Integer, comment="对应推荐表ID")
    aim = Column(String(255), comment="目标（如：减脂/增肌/正常）")
    grocery = Column(String(255), comment="食物类型（主食/正餐/辅食）")
    time = Column(String(255), comment="时间（早餐/午餐/晚餐）")
    food_id = Column(Integer, comment="食物ID")
    food_name = Column(String(255), comment="食物名称")
    weight = Column(Double, comment="用户偏好权重")

class UserExerciseRecommendList(Base):
    __tablename__ = "user_exercise_recommend_list"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    user_id = Column(Integer, nullable=False, comment="用户ID")
    exercise_recommend_list_id = Column(Integer, comment="推荐来源ID")
    exercise_id = Column(Integer, comment="运动ID")
    exercise_name = Column(String(255), comment="运动名称")
    exercise_category = Column(String(255), comment="运动类型/分类")
    calories_burn_rate = Column(String(255), comment="单位时间热量消耗")
    weight = Column(Double, comment="用户偏好权重")

# 创建数据库表
# Base.metadata.create_all(bind=engine)

# 数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
