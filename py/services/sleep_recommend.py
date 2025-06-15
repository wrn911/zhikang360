import os
import json
import requests
from flask import Flask, request
import threading
import time

# ==== 配置 ====
API_KEY = "4766ba4a488debd0b52a482e172f8bc0"  # ← 请填入你自己的 Suno API Key
CALLBACK_PORT = 8989
CALLBACK_PATH = "/callback"
CALLBACK_URL = f"https://064a-58-194-169-66.ngrok-free.app/callback "
SAVE_DIR = r"E:\zhikang360\files\music"  # 下载到 E 盘根目录
os.makedirs(SAVE_DIR, exist_ok=True)

# ==== Flask 应用 ====
app = Flask(__name__)

@app.route(CALLBACK_PATH, methods=["POST"])
def handle_callback():
    data = request.get_json()
    print("✅ 收到回调数据：", json.dumps(data, ensure_ascii=False, indent=2))

    if data.get("code") != 200 or data.get("data", {}).get("callbackType") != "complete":
        return {"msg": "忽略非完成阶段"}, 200

    for track in data["data"]["data"]:
        audio_url = track["audio_url"]
        title = track.get("title", track["id"]) + ".mp3"
        save_path = os.path.join(SAVE_DIR, title)

        try:
            print(f"⬇️ 正在下载：{audio_url}")
            audio_data = requests.get(audio_url)
            with open(save_path, "wb") as f:
                f.write(audio_data.content)
            print(f"🎉 已保存到：{save_path}")
        except Exception as e:
            print(f"❌ 下载失败：{e}")

    return {"msg": "已接收并处理回调"}, 200

def start_flask():
    app.run(host="0.0.0.0", port=CALLBACK_PORT)

# ==== 启动服务并发起请求 ====
if __name__ == "__main__":
    print("🚀 启动本地回调监听服务...")
    threading.Thread(target=start_flask, daemon=True).start()
    time.sleep(1)

    print("🎼 正在调用 Suno API 发起音乐生成请求...")

    url = "https://apibox.erweima.ai/api/v1/generate"
    payload = {
        "prompt": "一段平静舒缓的钢琴曲，带有柔和的旋律",
        "style": "古典",
        "title": "宁静钢琴冥想",
        "customMode": True,
        "instrumental": True,
        "model": "V3_5",
        "negativeTags": "重金属, 强节奏鼓点",
        "callBackUrl": CALLBACK_URL
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        print("🎯 请求发送成功，响应：", response.status_code)
        print(response.text)
    except Exception as e:
        print("❌ 请求失败：", e)

    # 防止主线程退出，等待回调
    input("⏳ 等待音乐生成回调中，按 Enter 键可手动退出...\n")


