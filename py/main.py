from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller import chat, knowledge_base, knowledge_file, session, food, music, foodRecommend, exerciseCheckin
from utils.jwt import jwt_auth_middleware
from controller.health_data_sync import router as health_sync_router
from utils.background_tasks import start_background_tasks, stop_background_tasks
import os
os.environ['MASTER_KEY'] = 'abcdef1234567890ABCDEF1234567890'  # 32字符密钥
app = FastAPI()

# 添加JWT认证中间件
app.middleware("http")(jwt_auth_middleware)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)

# 添加路由
app.include_router(chat.router)
app.include_router(knowledge_base.router)
app.include_router(knowledge_file.router)
app.include_router(session.router)
app.include_router(food.router)
app.include_router(music.router)
app.include_router(health_sync_router)

app.include_router(foodRecommend.router)
app.include_router(exerciseCheckin.router)

# 3. 添加应用启动和关闭事件处理器
@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    print("应用启动中...")
    # 启动后台任务
    start_background_tasks()
    print("应用启动完成")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    print("应用关闭中...")
    # 停止后台任务
    stop_background_tasks()
    print("应用关闭完成")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8000)

