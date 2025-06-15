


''''
def generate_music(prompt: str, style: str, title: str, user_id: int, music_type: str):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    prompt1 = "请一定要注意，生成的音频不要超过2分钟;" + prompt

    # Step 1: 发起音乐生成请求
    payload = {
        "prompt": prompt1,
        "style": style,
        "title": title,
        "customMode": True,
        "instrumental": True,
        "model": "V3_5",
        "callBackUrl": CALLBACK_URL  # ✅ 加回此字段
    }

    try:
        gen_res = requests.post(MUSIC_API_URL, headers=headers, json=payload)
        gen_json = gen_res.json()
        print("🎵 生成任务响应:", json.dumps(gen_json, indent=2, ensure_ascii=False))

        if gen_json.get("code") != 200:
            return {"code": 500, "msg": "音乐生成请求失败", "detail": gen_json}

        task_id = gen_json["data"]["taskId"]

        # Step 2: 查询任务状态（轮询最多30次，每2秒）
        print(f"⌛ 正在等待任务 {task_id} 完成生成...")
        for _ in range(60):
            query_res = requests.get(QUERY_API_URL, headers=headers, params={"taskId": task_id})
            query_json = query_res.json()
            print("🔍 状态查询:", query_json)

            if query_json.get("code") == 200:
                status = query_json["data"].get("status", "")
                if status == "SUCCESS":
                    tracks = query_json["data"]["response"]["sunoData"]
                    track = next((t for t in tracks if t.get("audioUrl")), None)

                    if not track:
                        return {"code": 500, "msg": "生成成功但未返8989"}

                    audio_url = track.get("sourceAudioUrl") or track.get("audioUrl")

                    headers = {
                        "User-Agent": "Mozilla/5.0",
                        "Accept": "*/*",
                    }

                    audio_data = requests.get(audio_url, headers=headers)

                    print(f"🔗 下载链接: {audio_url}")
                    print(f"📦 返回状态: {audio_data.status_code}, 内容大小: {len(audio_data.content)} 字节")

                    if audio_data.status_code != 200 or len(audio_data.content) < 1024:
                        return {"code": 500, "msg": "音频下载失败或内容为空"}

                    real_title = "aaa1"
                    duration = track.get("duration", 0)
                    title_mp3 = real_title + ".mp3"

                    # Step 3: 下载保存
                    user_dir = os.path.join(SAVE_ROOT, f"user_{user_id}")
                    os.makedirs(user_dir, exist_ok=True)
                    save_path = os.path.join(user_dir, title_mp3)
                    music_url = f"{LOCAL_BASE_URL}/user_{user_id}/{title_mp3}"

                    audio_data = requests.get(audio_url)
                    print(f"audio_data内容是{audio_data}")
                    if audio_data.status_code != 200:
                        print(f"❌ 音频下载失败，状态码: {audio_data.status_code}")
                        print(f"❗ 下载地址: {audio_url}")
                        return {"code": 500, "msg": "音频下载失败"}

                    if len(audio_data.content) < 1024:  # 小于1KB 的几乎是空文件
                        print(f"⚠️ 音频数据过小，可能无效（大小: {len(audio_data.content)} 字节）")
                        return {"code": 500, "msg": "下载成功但内容为空"}
                    print(f"📁 正在保存到: {save_path}")
                    with open(save_path, "wb") as f:
                        f.write(audio_data.content)
                    print("✅ 音频文件写入完成")

                    # Step 4: 写入数据库
                    db = next(get_db())
                    music_record = Music(
                        user_id=user_id,
                        title=real_title,
                        type=music_type,
                        duration=int(duration),
                        music_url=music_url,
                        play_count=0,  # ✅ 默认播放次数为0
                        create_time=datetime.now(),  # ✅ 当前时间
                        if_favorite=False  # ✅ 显式设置未收藏
                    )
                    db.add(music_record)
                    db.commit()
                    db.close()

                    return {
                        "code": 200,
                        "msg": "生成成功",
                        "title": real_title,
                        "duration": duration,
                        "music_url": music_url
                    }

                elif status in ["CREATE_TASK_FAILED", "GENERATE_AUDIO_FAILED", "SENSITIVE_WORD_ERROR"]:
                    return {"code": 500, "msg": f"音乐生成失败，状态：{status}"}

            time.sleep(5)

        return {"code": 504, "msg": "生成超时，请稍后重试"}

    except Exception as e:
        return {"code": 500, "msg": "异常", "error": str(e)}
'''

import os
import json
import aiohttp
import asyncio
import secrets
from datetime import datetime
from models.database import get_db, Music


API_KEY = "4766ba4a488debd0b52a482e172f8bc0"
MUSIC_API_URL = "https://apibox.erweima.ai/api/v1/generate"
QUERY_API_URL = "https://apibox.erweima.ai/api/v1/generate/record-info"
LOCAL_BASE_URL = "http://localhost:9090/files/music"
SAVE_ROOT = r"./files/music"
CALLBACK_URL = f"https://a16e-58-194-169-34.ngrok-free.app/callback"

async def generate_music(prompt: str, style: str, title: str, user_id: int, music_type: str):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    prompt1 = "请一定要注意，生成的音频不要超过2分钟;" + prompt
    payload = {
        "prompt": prompt1,
        "style": style,
        "title": title,
        "customMode": True,
        "instrumental": True,
        "model": "V3_5",
        "callBackUrl": CALLBACK_URL
    }

    try:
        async with aiohttp.ClientSession() as session:
            # Step 1: 发起音乐生成请求
            async with session.post(MUSIC_API_URL, headers=headers, json=payload) as gen_res:
                gen_json = await gen_res.json()
                print("🎵 生成任务响应:", json.dumps(gen_json, indent=2, ensure_ascii=False))

                if gen_json.get("code") != 200:
                    return {"code": 500, "msg": "音乐生成请求失败", "detail": gen_json}

                task_id = gen_json["data"]["taskId"]

            # Step 2: 查询状态（轮询）
            print(f"⌛ 正在等待任务 {task_id} 完成生成...")
            for _ in range(60):
                async with session.get(QUERY_API_URL, headers=headers, params={"taskId": task_id}) as query_res:
                    query_json = await query_res.json()
                    print("🔍 状态查询:", query_json)

                    if query_json.get("code") == 200:
                        status = query_json["data"].get("status", "")
                        if status == "SUCCESS":
                            tracks = query_json["data"]["response"]["sunoData"]
                            track = next((t for t in tracks if t.get("audioUrl")), None)
                            if not track:
                                return {"code": 500, "msg": "生成成功但未返回音频链接"}

                            audio_url = track.get("sourceAudioUrl") or track.get("audioUrl")
                            async with session.get(audio_url, headers={"User-Agent": "Mozilla/5.0"}) as audio_data:
                                content = await audio_data.read()
                                if audio_data.status != 200 or len(content) < 1024:
                                    return {"code": 500, "msg": "音频下载失败或内容为空"}

                                # 生成随机英文名，防止中文乱码
                                real_title = f"music_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{secrets.token_hex(3)}"
                                title_mp3 = real_title + ".mp3"
                                duration = track.get("duration", 0)

                                # 保存音频
                                user_dir = os.path.join(SAVE_ROOT, f"user_{user_id}")
                                os.makedirs(user_dir, exist_ok=True)
                                save_path = os.path.join(user_dir, title_mp3)
                                music_url = f"{LOCAL_BASE_URL}/user_{user_id}/{title_mp3}"

                                with open(save_path, "wb") as f:
                                    f.write(content)

                                print("✅ 音频保存完成")

                                # 写入数据库（仍用同步）
                                db = next(get_db())
                                music_record = Music(
                                    user_id=user_id,
                                    title=title,
                                    type=music_type,
                                    duration=int(duration),
                                    music_url=music_url,
                                    play_count=0,
                                    create_time=datetime.now(),
                                    if_favorite=False
                                )
                                db.add(music_record)
                                db.commit()
                                db.close()

                                return {
                                    "code": 200,
                                    "msg": "生成成功",
                                    "title": title,
                                    "duration": duration,
                                    "music_url": music_url
                                }

                        elif status in ["CREATE_TASK_FAILED", "GENERATE_AUDIO_FAILED", "SENSITIVE_WORD_ERROR"]:
                            return {"code": 500, "msg": f"音乐生成失败，状态：{status}"}

                await asyncio.sleep(5)

            return {"code": 504, "msg": "生成超时，请稍后重试"}

    except Exception as e:
        return {"code": 500, "msg": "异常", "error": str(e)}






