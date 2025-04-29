import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests
from openai import OpenAI
import json

app = Flask(__name__)
CORS(app)

# 配置 MySQL 数据库连接（与现有项目保持一致）
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:d731028031@localhost:3306/zhikang360'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {
        'charset': 'utf8mb4'
    }
}

db = SQLAlchemy(app)

# 定义运动表模型
class Exercise(db.Model):
    __tablename__ = 'exercise'
    exercise_id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String(100), nullable=False)
    exercise_category = db.Column(db.String(50))
    calories_burn_rate = db.Column(db.Integer)

# 大模型API配置
LLM_API_URL = "http://10.2.8.77:3000/v1"
LLM_API_KEY = "sk-93nWYhI8SrnXad5m9932CeBdDeDf4233B21d93D217095f22"

def get_exercise_recommendations(user_info=None):
    """
    调用大模型API获取运动推荐
    :param user_info: 用户信息，可以包含用户偏好、身体状况等
    :return: 推荐的运动列表
    """
    # 从数据库获取所有运动信息
    exercises = Exercise.query.all()

    # 构建运动信息列表
    exercise_list = []
    for exercise in exercises:
        exercise_info = {
            "id": exercise.exercise_id,
            "name": exercise.exercise_name,
            "category": exercise.exercise_category or "未分类",
            "calories_burn_rate": exercise.calories_burn_rate or 0
        }
        exercise_list.append(exercise_info)

    # 构建提示词
    prompt = f"""
    你是一个专业的运动推荐助手。请根据用户情况，从以下运动列表中推荐3-5项适合的运动：
    
    可选运动列表：
    {[f"{e['name']}（类别：{e['category']}，单位时间消耗卡路里：{e['calories_burn_rate']}）" for e in exercise_list]}
    
    用户信息：{user_info if user_info else '无特殊要求'}
    
    请以JSON格式返回推荐的运动，格式为：
    {{
        "recommendations": [
            {{
                "exercise_id": 运动ID,
                "exercise_name": "运动名称",
                "reason": "推荐理由"
            }},
            ...
        ]
    }}
    """

    # 调用大模型API
    messages = [
        {"role": "system", "content": "你是一个专业的运动健康顾问，擅长根据用户情况推荐合适的运动。"},
        {"role": "user", "content": prompt}
    ]
    client = OpenAI(api_key="sk-93nWYhI8SrnXad5m9932CeBdDeDf4233B21d93D217095f22", base_url="http://10.2.8.77:3000/v1")
    response = client.chat.completions.create(
        model="DeepSeek-R1",
        messages=messages
    )

    try:
        result = json.loads(response)

        # 解析大模型返回的结果
        # 注意：这里的解析逻辑可能需要根据实际API返回格式调整
        if 'choices' in result and len(result['choices']) > 0:
            content = result['choices'][0]['message']['content']
            print(content)

            # 尝试解析JSON格式的推荐结果
            try:
                # 查找JSON内容（可能嵌在文本中）
                import re
                json_match = re.search(r'\{\s*"recommendations".*\}', content, re.DOTALL)
                if json_match:
                    recommendations_json = json.loads(json_match.group())
                    return {"code": 200, "msg": "推荐成功", "data": recommendations_json}
                else:
                    # 如果没有找到JSON格式，尝试直接解析整个内容
                    recommendations_json = json.loads(content)
                    return {"code": 200, "msg": "推荐成功", "data": recommendations_json}
            except json.JSONDecodeError:
                # 如果JSON解析失败，返回原始文本
                return {"code": 200, "msg": "推荐成功", "data": {"text": content}}
        else:
            return {"code": 500, "msg": "大模型未返回有效结果"}

    except requests.exceptions.RequestException as e:
        return {"code": 500, "msg": f"请求失败: {str(e)}"}
    except Exception as e:
        return {"code": 500, "msg": f"处理失败: {str(e)}"}

@app.route('/api/exercise/recommend', methods=['POST'])
def recommend_exercise():
    """
    运动推荐API接口
    请求体可以包含用户信息，用于个性化推荐
    """
    try:
        print("运动推荐API接口")
        data = request.json or {}
        user_info = data.get('user_info', '')
        
        # 调用推荐函数
        result = get_exercise_recommendations(user_info)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"code": 500, "msg": f"服务器错误: {str(e)}"})

# 简单的健康检查接口
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "运动推荐服务正常运行中"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # app.run(debug=True, port=5001)  # 使用不同端口避免与其他服务冲突
        result = get_exercise_recommendations()