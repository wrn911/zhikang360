from sqlalchemy.orm import Session
from models.database import (
    get_db, UserKnowledgeStatus, KnowledgeUpdateTask
)
from services.health_data_aggregator import aggregate_user_health_data
from services.knowledge_manager import knowledge_manager  # 导入统一管理服务
from datetime import datetime
import traceback


def update_user_health_knowledge(user_id: int, db: Session) -> bool:
    """更新用户健康知识库 - 使用统一管理服务"""
    try:
        print(f"开始更新用户 {user_id} 的健康知识库")

        # 1. 生成健康档案内容
        profile_content = aggregate_user_health_data(user_id, db)

        if not profile_content.strip():
            print(f"用户 {user_id} 的健康档案内容为空，跳过更新")
            return False

        # 2. 使用统一管理服务更新健康档案
        result = knowledge_manager.update_health_profile(
            user_id=user_id,
            profile_content=profile_content,
            db=db
        )

        if result["success"]:
            print(f"用户 {user_id} 的健康知识库更新完成")
            return True
        else:
            print(f"用户 {user_id} 健康知识库更新失败: {result['error']}")
            return False

    except Exception as e:
        print(f"更新用户 {user_id} 健康知识库时出错: {str(e)}")
        traceback.print_exc()
        return False


def create_update_task(user_id: int, db: Session) -> bool:
    """创建知识库更新任务"""
    try:
        # 检查是否已有待处理的任务
        existing_task = db.query(KnowledgeUpdateTask).filter(
            KnowledgeUpdateTask.user_id == user_id,
            KnowledgeUpdateTask.status.in_(["pending", "processing"])
        ).first()

        if existing_task:
            print(f"用户 {user_id} 已有待处理的更新任务，跳过创建")
            return True

        # 创建新任务
        task = KnowledgeUpdateTask(
            user_id=user_id,
            task_type="health_data_sync",
            status="pending"
        )
        db.add(task)

        # 更新用户状态为待更新
        status_record = db.query(UserKnowledgeStatus).filter(
            UserKnowledgeStatus.user_id == user_id
        ).first()

        if status_record:
            status_record.update_status = "pending"
            status_record.last_health_update = datetime.now()
            status_record.updated_at = datetime.now()
        else:
            status_record = UserKnowledgeStatus(
                user_id=user_id,
                update_status="pending",
                last_health_update=datetime.now()
            )
            db.add(status_record)

        db.commit()
        print(f"为用户 {user_id} 创建了知识库更新任务")
        return True

    except Exception as e:
        print(f"创建用户 {user_id} 更新任务时出错: {str(e)}")
        db.rollback()
        return False


def process_pending_tasks():
    """处理待更新的任务 - 使用正确的数据库连接管理"""
    db_generator = get_db()
    db = next(db_generator)

    try:
        # 获取待处理任务（最多3个）
        pending_tasks = db.query(KnowledgeUpdateTask).filter(
            KnowledgeUpdateTask.status == "pending"
        ).order_by(KnowledgeUpdateTask.created_at.asc()).limit(3).all()

        if not pending_tasks:
            print("没有待处理的知识库更新任务")
            return

        print(f"找到 {len(pending_tasks)} 个待处理任务")

        for task in pending_tasks:
            process_single_task(task, db)

    except Exception as e:
        print(f"处理待更新任务时出错: {str(e)}")
        traceback.print_exc()
    finally:
        try:
            db.close()
        except:
            pass


def process_single_task(task: KnowledgeUpdateTask, db: Session):
    """处理单个任务"""
    try:
        print(f"开始处理任务 {task.id}，用户 {task.user_id}")

        # 标记任务为处理中
        task.status = "processing"
        task.processed_at = datetime.now()

        # 更新用户状态
        status_record = db.query(UserKnowledgeStatus).filter(
            UserKnowledgeStatus.user_id == task.user_id
        ).first()
        if status_record:
            status_record.update_status = "updating"

        db.commit()

        # 执行知识库更新
        success = update_user_health_knowledge(task.user_id, db)

        if success:
            task.status = "completed"
            task.retry_count = 0
            task.error_message = None
            if status_record:
                status_record.update_status = "idle"
            print(f"任务 {task.id} 执行成功")
        else:
            task.status = "failed"
            task.retry_count += 1
            task.error_message = "知识库更新失败"
            if status_record:
                status_record.update_status = "idle"
            print(f"任务 {task.id} 执行失败，重试次数: {task.retry_count}")

            # 如果重试次数超过3次，标记为永久失败
            if task.retry_count >= 3:
                task.status = "permanently_failed"
                print(f"任务 {task.id} 重试次数过多，标记为永久失败")

        db.commit()

    except Exception as e:
        print(f"处理任务 {task.id} 时出错: {str(e)}")
        traceback.print_exc()

        try:
            task.status = "failed"
            task.retry_count += 1
            task.error_message = str(e)

            # 重置用户状态
            status_record = db.query(UserKnowledgeStatus).filter(
                UserKnowledgeStatus.user_id == task.user_id
            ).first()
            if status_record:
                status_record.update_status = "idle"

            db.commit()
        except Exception as commit_error:
            print(f"提交错误状态时出错: {commit_error}")
            db.rollback()