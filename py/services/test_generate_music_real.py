import os
import pytest
from services.music_services import generate_music  # 确保 import 路径正确
from models.database import get_db, Music

# 测试参数
USER_ID = 2
TITLE = "宁静的民谣"
PROMPT = "请注意生成的音乐时长一定不要超过2分钟，一段舒缓宁静的钢琴旋律，适合睡前放松"
STYLE = "古典"
TYPE = "解压"
SAVE_ROOT = rf"E:\zhikang360\springboot\files\music\user_{USER_ID}"
SAVE_FILE = os.path.join(SAVE_ROOT, f"{TITLE}.mp3")


@pytest.fixture(autouse=True)
def clean_music_file():
    # 测试前后清理本地文件
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
    yield
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)


def test_generate_music_real():
    # 调用生成函数（会等待音乐生成完成）
    result = generate_music(
        prompt=PROMPT,
        style=STYLE,
        title=TITLE,
        user_id=USER_ID,
        music_type=TYPE
    )

    print("🎯 生成结果：", result)

    # 验证返回内容
    assert result["code"] == 200, f"生成失败: {result}"
    assert "music_url" in result
    assert "duration" in result
    assert result["title"] == TITLE

    # 验证文件是否存在
    assert os.path.exists(SAVE_FILE), "音频文件未保存成功"

    # 验证数据库是否写入
    db = next(get_db())
    music = db.query(Music).filter(Music.user_id == USER_ID, Music.title == TITLE).first()
    db.close()

    assert music is not None, "数据库中未找到记录"
    assert music.music_url.endswith(".mp3")
    assert music.duration > 0

