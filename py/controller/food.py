import base64
import json
import os
import re
import requests
from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter, Form, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from models.database import get_db, Food, FoodCheckin

router = APIRouter(prefix="/food", tags=["food"])


def call_glm4v_for_weight(image_base64: str, food_name: str, distance_cm: int = 30, max_retry: int = 3) -> float:
    """
    调用GLM-4V模型识别指定食物的重量，自动重试机制

    参数:
        image_base64: 图片的base64编码字符串
        food_name: 食物名称
        distance_cm: 摄像头与食物的距离(厘米)
        max_retry: 最多重试次数，默认3次

    返回:
        float: 识别出的食物重量(克)

    异常:
        HTTPException: 模型调用失败或多次返回无效结果
    """
    prompt = (
        f"请识别图片中'{food_name}'的重量，单位为克。"
        f"摄像头与食物的距离为{distance_cm}厘米。"
        f"图片中的食物是：{food_name}，请根据这个信息准确估算其重量。"
        f"请考虑{food_name}的常见分量大小来判断重量。"
        f"只返回一个数字，表示重量的克数，不要其他文字说明。"
        f"例如：如果重量是150克，直接返回'150'。"
    )

    with open('settings.json') as settings_file:
        glm_config = json.load(settings_file)['glm']
        GLM4V_API_KEY = glm_config['api_key']
        GLM4V_API_URL = glm_config['url']
        GLM4V_MODEL = "glm-4v-flash"

    headers = {
        "Authorization": f"Bearer {GLM4V_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GLM4V_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    }

    for attempt in range(1, max_retry + 1):
        try:
            resp = requests.post(
                GLM4V_API_URL + "/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )

            if resp.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail=f"模型调用失败: {resp.text}"
                )

            data = resp.json()
            result = data["choices"][0]["message"]["content"].strip()
            print(f"[尝试 {attempt}] 模型返回内容：{result}")

            # 正则提取重量数字
            numbers = re.findall(r'\d+\.?\d*', result)
            if numbers:
                weight = float(numbers[0])
                return weight
            else:
                print(f"[尝试 {attempt}] 无法提取重量数字，结果为：{result}")

        except (requests.RequestException, KeyError, IndexError, ValueError) as e:
            print(f"[尝试 {attempt}] 调用异常或解析失败: {str(e)}")

    # 所有尝试都失败
    raise HTTPException(
        status_code=500,
        detail=f"已重试 {max_retry} 次，仍无法获取有效重量结果。"
    )



@router.post("/checkin")
async def food_checkin(
        food_id: str = Form(...),
        checkin_type: str = Form(...),
        file: UploadFile = File(...),
        request: Request = None,
        db: Session = Depends(get_db)
):
    """
    食物打卡接口：接收食物id、餐别和图片，识别重量，查营养，写入food_checkin表

    参数:
        food_id: 食物ID，关联food表
        checkin_type: 餐别字符串（早餐/午餐/晚餐）
        file: 上传的食物图片文件
        db: 数据库会话

    返回:
        JSONResponse: 包含打卡成功信息和营养数据
    """

    # 1. 获取用户ID
    user_id = None

    # 优先从request.state.user_payload获取（如果request存在）
    if request and hasattr(request.state, "user_payload") and request.state.user_payload:
        user_id = request.state.user_payload.get("aud", "-").split("-")[0]

    # 兜底从BaseContext获取
    if not user_id:
        try:
            from utils.jwt import BaseContext
            user_id = BaseContext.current_user_id
        except:
            # 如果都获取不到，使用默认用户ID或抛出异常
            # 临时方案：使用默认用户ID 1（仅用于测试）
            user_id = 1
            # 生产环境应该抛出异常：
            # raise HTTPException(status_code=401, detail="无法获取用户身份")

    user_id = int(user_id)

    # 2. 验证和转换food_id
    try:
        food_id = int(food_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"food_id必须是整数，收到: {food_id}"
        )

    # 3. 验证餐别
    valid_checkin_types = ["早餐", "午餐", "晚餐"]
    if checkin_type not in valid_checkin_types:
        raise HTTPException(
            status_code=400,
            detail=f"餐别必须是以下之一: {', '.join(valid_checkin_types)}"
        )

    # 4. 查询食物信息
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        # 增加调试信息
        total_foods = db.query(Food).count()
        raise HTTPException(
            status_code=404,
            detail=f"食物ID {food_id} 不存在。数据库中共有 {total_foods} 个食物记录"
        )

    # 获取食物名称，用于后续的大模型识别
    food_name = food.name

    # 5. 验证文件类型
    if not file.filename:
        raise HTTPException(status_code=400, detail="请选择要上传的文件")

    # 检查文件扩展名
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    file_ext = os.path.splitext(file.filename.lower())[1]
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式 {file_ext}。支持的格式: {', '.join(allowed_extensions)}"
        )

    # 6. 读取图片并转换为base64
    try:
        img_bytes = await file.read()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"图片读取失败: {str(e)}"
        )

    # 7. 调用大模型识别重量（传入食物名称）
    try:
        weight = call_glm4v_for_weight(img_base64, food_name)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"重量识别失败: {str(e)}"
        )

    # 8. 计算营养摄入量（基于每100g的营养值）
    def calc_nutrition(nutrition_per_100g):
        """计算实际营养摄入量"""
        if nutrition_per_100g is None:
            return 0.0
        return round(nutrition_per_100g * weight / 100.0, 2)

    calories_ate = calc_nutrition(food.calories)
    carbohydrates_ate = calc_nutrition(food.carbohydrates)
    fat_ate = calc_nutrition(food.fat)
    protein_ate = calc_nutrition(food.protein)
    fiber_ate = calc_nutrition(food.fiber)

    # 9. 创建打卡记录
    try:
        checkin = FoodCheckin(
            user_id=user_id,
            checkin_type=checkin_type,
            food_id=food.id,
            food_name=food.name,
            gram_ate=int(weight),
            calories_ate=calories_ate,
            carbohydrates_ate=carbohydrates_ate,
            fat_ate=fat_ate,
            protein_ate=protein_ate,
            fiber_ate=fiber_ate,
        )

        db.add(checkin)
        db.commit()
        db.refresh(checkin)

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"数据库操作失败: {str(e)}"
        )

    # 10. 返回成功响应
    return JSONResponse(content={
        "statusCode":200,
        "success": True,
        "message": "食物打卡成功",
        "data": {
            "checkin_id": checkin.checkin_id,
            "food_name": food.name,
            "checkin_type": checkin_type,
            "weight_grams": int(weight),
            "nutrition": {
                "calories": calories_ate,
                "carbohydrates": carbohydrates_ate,
                "fat": fat_ate,
                "protein": protein_ate,
                "fiber": fiber_ate
            }
        }
    })