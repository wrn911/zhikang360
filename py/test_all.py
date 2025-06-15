import pytest
from datetime import datetime
from services.food_recommend import generate_three_meals_recommendation

@pytest.mark.asyncio
async def test_generate_three_meals():
    user_id = 2  # 请替换为你数据库中真实存在的用户ID
    now = datetime.now()

    result = await generate_three_meals_recommendation(user_id, now)

    assert "recommendations" in result
    assert all(meal in result["recommendations"] for meal in ["早餐", "午餐", "晚餐"])

    all_foods = [
        item["food_name"]
        for items in result["recommendations"].values()
        for item in items
    ]
    assert len(all_foods) == len(set(all_foods)), "三餐中存在重复食物！"

