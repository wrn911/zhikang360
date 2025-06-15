import asyncio
import threading
import time
from services.user_knowledge_updater import process_pending_tasks
from datetime import datetime


class BackgroundTaskManager:
    """后台任务管理器"""

    def __init__(self, interval=300):  # 默认5分钟
        self.interval = interval  # 扫描间隔（秒）
        self.running = False
        self.thread = None

    def start(self):
        """启动后台任务"""
        if self.running:
            print("后台任务已经在运行中")
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_background_tasks, daemon=True)
        self.thread.start()
        print(f"后台任务管理器已启动，扫描间隔: {self.interval}秒")

    def stop(self):
        """停止后台任务"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=10)
        print("后台任务管理器已停止")

    def _run_background_tasks(self):
        """运行后台任务的主循环"""
        while self.running:
            try:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行后台任务扫描")

                # 处理待更新的知识库任务
                process_pending_tasks()

                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 后台任务扫描完成")

            except Exception as e:
                print(f"后台任务执行时出错: {str(e)}")
                import traceback
                traceback.print_exc()

            # 等待下一次扫描
            for i in range(self.interval):
                if not self.running:
                    break
                time.sleep(1)


# 全局任务管理器实例
task_manager = BackgroundTaskManager()


def start_background_tasks():
    """启动后台任务（在应用启动时调用）"""
    task_manager.start()


def stop_background_tasks():
    """停止后台任务（在应用关闭时调用）"""
    task_manager.stop()


# 用于手动测试的函数
def test_background_tasks():
    """测试后台任务功能"""
    print("开始测试后台任务...")
    process_pending_tasks()
    print("后台任务测试完成")


if __name__ == "__main__":
    # 直接运行此文件进行测试
    test_background_tasks()