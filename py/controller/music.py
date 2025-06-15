from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from models.database import Music, get_db
from utils.jwt import BaseContext
from services.music_services import generate_music
from fastapi.responses import JSONResponse
from fastapi import BackgroundTasks
from datetime import datetime, timedelta
router = APIRouter(prefix="/music", tags=["music"])

class MusicGenerateRequest(BaseModel):
    prompt: str = Field(..., description="生成音乐的文本提示")
    style: str = Field(default="流行", description="音乐风格，如：流行、古典")
    title: str = Field(default="AI音乐", description="音乐标题")
    type: str = Field(default="个人导入", description="音乐类型")



@router.post("/generate")
def generate_music_api(
    request: MusicGenerateRequest,
    background_tasks: BackgroundTasks
):
    user_id = BaseContext.current_user_id

    # ✅ 提交后台任务（不等待）
    background_tasks.add_task(
        generate_music,
        request.prompt,
        request.style,
        request.title,
        user_id,
        request.type
    )

    # ✅ 立即返回
    return JSONResponse(status_code=200, content={"message": "音乐生成中，请稍后查看"})




@router.get("/status")
def check_music_status():
    db = next(get_db())

    one_minute_ago = datetime.now() - timedelta(minutes=1)

    latest_music = (
        db.query(Music)
        .filter(
            Music.user_id == BaseContext.current_user_id,
            Music.create_time >= one_minute_ago  # ✅ 限制 1 分钟内
        )
        .order_by(Music.create_time.desc())
        .first()
    )

    if not latest_music:
        return JSONResponse(status_code=500, content={"message": "音乐生成中，请稍后查看"})

    return JSONResponse(status_code=200, content={"message": "音乐生成完毕"})





