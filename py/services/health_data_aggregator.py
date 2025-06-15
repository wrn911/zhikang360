from sqlalchemy.orm import Session
from models.database import (
    UserInfo, FoodInfo, SportInfo, IllnessInfo, SleepInfo,
    FoodCheckin, ExerciseCheckin, User
)
from datetime import datetime, timedelta
from typing import Optional
import os


def calculate_age(birth_date):
    """计算年龄"""
    if not birth_date:
        return None
    today = datetime.now().date()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def calculate_bmi(height, weight):
    """计算BMI"""
    if not height or not weight:
        return None
    height_m = float(height) / 100  # 转换为米
    bmi = float(weight) / (height_m ** 2)
    return round(bmi, 1)


def get_bmi_status(bmi):
    """获取BMI状态描述"""
    if not bmi:
        return "未知"
    if bmi < 18.5:
        return "偏瘦"
    elif bmi < 24:
        return "正常"
    elif bmi < 28:
        return "超重"
    else:
        return "肥胖"


def get_recent_food_analysis(user_id: int, db: Session, days: int = 30):
    """分析最近的饮食记录"""
    cutoff_date = datetime.now() - timedelta(days=days)

    food_records = db.query(FoodCheckin).filter(
        FoodCheckin.user_id == user_id,
        FoodCheckin.create_time >= cutoff_date
    ).all()

    if not food_records:
        return "最近30天无饮食记录"

    # 统计数据
    total_records = len(food_records)
    total_calories = sum(record.calories_ate or 0 for record in food_records)
    avg_daily_calories = round(total_calories / days, 0) if days > 0 else 0

    # 餐别统计
    meal_counts = {'早餐': 0, '午餐': 0, '晚餐': 0}
    for record in food_records:
        meal_type = record.checkin_type
        if meal_type in meal_counts:
            meal_counts[meal_type] += 1

    # 常见食物
    food_frequency = {}
    for record in food_records:
        food_name = record.food_name
        food_frequency[food_name] = food_frequency.get(food_name, 0) + 1

    top_foods = sorted(food_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
    top_foods_str = "、".join([food[0] for food in top_foods])

    analysis = f"""最近{days}天饮食分析：
- 总记录数：{total_records}次
- 平均每日摄入：{avg_daily_calories}卡路里
- 早餐记录：{meal_counts['早餐']}次，午餐记录：{meal_counts['午餐']}次，晚餐记录：{meal_counts['晚餐']}次
- 常见食物：{top_foods_str}"""

    return analysis


def get_recent_exercise_analysis(user_id: int, db: Session, days: int = 30):
    """分析最近的运动记录"""
    cutoff_date = datetime.now() - timedelta(days=days)

    exercise_records = db.query(ExerciseCheckin).filter(
        ExerciseCheckin.user_id == user_id,
        ExerciseCheckin.create_time >= cutoff_date,
        ExerciseCheckin.checkin_date.isnot(None)  # 只统计已完成的运动
    ).all()

    if not exercise_records:
        return "最近30天无运动记录"

    # 统计数据
    total_records = len(exercise_records)
    total_duration = sum(record.duration or 0 for record in exercise_records)
    total_calories = sum(record.calories_burned or 0 for record in exercise_records)
    avg_daily_calories = round(total_calories / days, 0) if days > 0 else 0

    # 运动类型统计
    exercise_frequency = {}
    for record in exercise_records:
        exercise_name = record.exercise_name
        exercise_frequency[exercise_name] = exercise_frequency.get(exercise_name, 0) + 1

    top_exercises = sorted(exercise_frequency.items(), key=lambda x: x[1], reverse=True)[:3]
    exercise_distribution = []
    for exercise, count in top_exercises:
        percentage = round(count / total_records * 100, 0)
        exercise_distribution.append(f"{exercise}({percentage}%)")

    exercise_dist_str = "、".join(exercise_distribution)
    avg_duration = round(total_duration / total_records, 0) if total_records > 0 else 0

    analysis = f"""最近{days}天运动分析：
- 运动次数：{total_records}次
- 总运动时长：{total_duration}分钟，平均每次：{avg_duration}分钟
- 总消耗热量：{total_calories}卡路里，平均每日：{avg_daily_calories}卡路里
- 主要运动类型：{exercise_dist_str}"""

    return analysis


def aggregate_user_health_data(user_id: int, db: Session) -> str:
    """聚合用户健康数据生成档案"""

    # 获取基本信息
    user_info = db.query(UserInfo).filter(UserInfo.user_id == user_id).first()
    user = db.query(User).filter(User.id == user_id).first()

    # 获取各种健康信息
    food_info = db.query(FoodInfo).filter(FoodInfo.user_id == user_id).first()
    sport_info = db.query(SportInfo).filter(SportInfo.user_id == user_id).first()
    illness_info = db.query(IllnessInfo).filter(IllnessInfo.user_id == user_id).first()
    sleep_info = db.query(SleepInfo).filter(SleepInfo.user_id == user_id).order_by(SleepInfo.create_time.desc()).first()

    # 生成档案内容
    profile_lines = []
    profile_lines.append("=== 用户健康档案 ===")
    profile_lines.append(f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    profile_lines.append(f"用户ID：{user_id}")
    if user:
        profile_lines.append(f"用户名：{user.username}")
    profile_lines.append("")

    # 基本信息
    profile_lines.append("【基本信息】")
    if user_info:
        gender = user_info.gender if user_info.gender else "未知"
        age = calculate_age(user_info.birth_date) if user_info.birth_date else "未知"
        height = f"{user_info.height}cm" if user_info.height else "未填写"
        weight = f"{user_info.weight}kg" if user_info.weight else "未填写"

        profile_lines.append(f"性别：{gender}")
        profile_lines.append(f"年龄：{age}岁" if age != "未知" else "年龄：未填写")
        profile_lines.append(f"身高：{height}，体重：{weight}")

        # 计算BMI
        if user_info.height and user_info.weight:
            bmi = calculate_bmi(user_info.height, user_info.weight)
            bmi_status = get_bmi_status(bmi)
            profile_lines.append(f"BMI：{bmi}（{bmi_status}）")

        if user_info.blood_pressure:
            profile_lines.append(f"血压：{user_info.blood_pressure}")
        if user_info.blood_sugar:
            profile_lines.append(f"血糖：{user_info.blood_sugar}mmol/L")
    else:
        profile_lines.append("基本信息未填写")
    profile_lines.append("")

    # 健康状况
    profile_lines.append("【健康状况】")
    if illness_info:
        allergy_info = []
        if illness_info.allergy_type:
            allergy_info.append(f"过敏类型：{illness_info.allergy_type}")
        if illness_info.allergy_details:
            allergy_info.append(f"过敏详情：{illness_info.allergy_details}")

        if allergy_info:
            profile_lines.extend(allergy_info)
        else:
            profile_lines.append("过敏情况：无")

        chronic = illness_info.chronic_diseases if illness_info.chronic_diseases else "无"
        profile_lines.append(f"慢性疾病：{chronic}")

        if illness_info.health_issues:
            profile_lines.append(f"其他健康问题：{illness_info.health_issues}")
    else:
        profile_lines.append("健康状况信息未填写")
    profile_lines.append("")

    # 饮食偏好与记录
    profile_lines.append("【饮食偏好与习惯】")
    if food_info:
        preferences = food_info.preferences if food_info.preferences else "未填写"
        avoids = food_info.avoids if food_info.avoids else "无特殊忌口"
        willingness = food_info.willingness if food_info.willingness else "未填写"

        profile_lines.append(f"饮食偏好：{preferences}")
        profile_lines.append(f"忌口食物：{avoids}")
        profile_lines.append(f"配合意愿：{willingness}")
    else:
        profile_lines.append("饮食偏好信息未填写")

    # 添加饮食记录分析
    food_analysis = get_recent_food_analysis(user_id, db)
    profile_lines.append(food_analysis)
    profile_lines.append("")

    # 运动偏好与记录
    profile_lines.append("【运动偏好与习惯】")
    if sport_info:
        preferences = sport_info.preferences if sport_info.preferences else "未填写"
        weaknesses = sport_info.weaknesses if sport_info.weaknesses else "无特别厌恶的运动"
        experience = sport_info.experience if sport_info.experience else "未填写"
        intensity = sport_info.intensity if sport_info.intensity else "未填写"
        free_times = sport_info.free_times if sport_info.free_times else "未填写"
        willingness = sport_info.willingness if sport_info.willingness else "未填写"

        profile_lines.append(f"运动偏好：{preferences}")
        profile_lines.append(f"讨厌的运动：{weaknesses}")
        profile_lines.append(f"健身经验：{experience}")
        profile_lines.append(f"强度偏好：{intensity}")
        profile_lines.append(f"空闲时间：{free_times}")
        profile_lines.append(f"配合意愿：{willingness}")
    else:
        profile_lines.append("运动偏好信息未填写")

    # 添加运动记录分析
    exercise_analysis = get_recent_exercise_analysis(user_id, db)
    profile_lines.append(exercise_analysis)
    profile_lines.append("")

    # 睡眠状况
    profile_lines.append("【睡眠状况】")
    if sleep_info:
        sleep_time = sleep_info.sleep_time if sleep_info.sleep_time else "未填写"
        wakeup_time = sleep_info.wakeup_time if sleep_info.wakeup_time else "未填写"
        emotions = sleep_info.emotions if sleep_info.emotions else "未填写"

        profile_lines.append(f"睡眠时间：{sleep_time}")
        profile_lines.append(f"起床时间：{wakeup_time}")
        profile_lines.append(f"情绪状态：{emotions}")
    else:
        profile_lines.append("睡眠信息未填写")

    profile_lines.append("")
    profile_lines.append("=== 档案结束 ===")

    return "\n".join(profile_lines)


def save_health_profile(user_id: int, profile_content: str) -> str:
    """保存健康档案到文件"""
    # 确保目录存在
    profiles_dir = os.path.join(os.getcwd(), "user_profiles")
    os.makedirs(profiles_dir, exist_ok=True)

    # 生成文件路径
    filename = f"user_{user_id}_health_profile.txt"
    file_path = os.path.join(profiles_dir, filename)

    # 保存文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(profile_content)

    return file_path