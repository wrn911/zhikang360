import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests
import uuid

app = Flask(__name__)
CORS(app)

# 配置 MySQL 数据库连接（根据实际情况修改）
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/zhikang360?useUnicode=true&characterEncoding=utf-8&allowMultiQueries=true&useSSL=false&serverTimezone=GMT%2b8&allowPublicKeyRetrieval=true'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # 存放上传文件的目录

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

class BadgeStandard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    name = db.Column(db.String(100))
    days = db.Column(db.Integer)
    description = db.Column(db.Text)
    url = db.Column(db.String(255))


# 替换为您的API密钥
API_KEY = "your_api_key_here"


def generate_image(prompt):
    # API端点
    url = "https://api.doubao.com/v2/ai-img/text-to-image"

    # 请求头
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 请求参数
    payload = {
        "text": prompt,
        "style_id": 0,  # 风格ID（0-无风格，1-卡通，2-插画等）
        "width": 512,
        "height": 512,
        "num": 1  # 生成图片数量
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # 检查HTTP错误状态码

        result = response.json()
        if result.get("code") == 0:
            # 提取图片URL（注意可能返回多个结果）
            image_urls = [item["url"] for item in result["data"]]
            return {"code": 200, "msg": "生成成功", "image_urls": image_urls}
        else:
            return {"code": result.get("code", 500), "msg": result.get("msg", "生成失败")}

    except requests.exceptions.RequestException as e:
        return {"code": 500, "msg": f"请求失败: {str(e)}"}


# 使用示例
prompt = "赛博朋克风格的城市夜景，霓虹灯光闪烁"
result = generate_image(prompt)
print(result)

@app.route('/py/create', methods=['POST'])
def create_badge():
    data = request.json
    badge_id = data.get('id')
    suggestion = data.get('suggestion', '')

    # 根据勋章ID获取勋章信息
    badge = BadgeStandard.query.get(badge_id)
    if not badge:
        return jsonify(code='404', msg='勋章未找到')

    # 构造提示词
    prompt = f"生成一个{badge.type}类别的勋章图片，名称为'{badge.name}'，描述为'{badge.description}'，达标天数为{badge.days}天。{suggestion}"

    # 调用豆包API生成图片（此处为示例，实际调用方式根据豆包API文档进行）
    # 假设豆包API返回图片的URL
    response = requests.post('https://doubao-api.com/generate', json={'prompt': prompt})
    if response.status_code != 200:
         return jsonify(code='500', msg='AI生成图片失败')
    ai_image_url = response.json().get('image_url')

    # 模拟生成图片URL（实际应替换为豆包API返回的URL）
    ai_image_url = f"https://via.placeholder.com/150x150.png?text={badge.name}+AI+Generated"

    # 下载图片并保存到本地
    image_response = requests.get(ai_image_url)
    if image_response.status_code != 200:
        return jsonify(code='500', msg='下载图片失败')
    image_data = image_response.content
    filename = f"{uuid.uuid4().hex}.png"
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(save_path, 'wb') as f:
        f.write(image_data)

    # 构造本地图片URL
    local_url = f"/{app.config['UPLOAD_FOLDER']}/{filename}"

    # 更新勋章图片URL
    badge.url = local_url
    db.session.commit()

    return jsonify(code='200', msg='AI生成图片成功', data={'url': local_url})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

