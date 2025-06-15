# services/intent_recognizer.py (改进版本)
import re
from typing import Optional, Dict, Any, List

# 意图规则配置 - 简化并优化关键词
INTENT_RULES = {
    "diet_record": {
        "name": "饮食记录",
        "keywords": [
            "饮食", "吃饭", "食物", "营养", "卡路里", "记录饮食", "饮食打卡",
            "吃什么", "吃了", "早餐", "午餐", "晚餐", "零食", "喝水",
            "食谱", "饮食习惯", "饮食管理", "饮食计划", "饮食记录"
        ],
        "high_priority_keywords": ["饮食记录", "饮食打卡", "记录饮食", "饮食管理"],  # 高权重关键词
        "negative_keywords": ["不想吃", "不要", "拒绝", "不饿", "没胃口"],
        "action": {
            "type": "navigate",
            "url": "/pages/food/food1",
            "title": "去记录饮食",
            "icon": "🍽️",
            "description": "记录您的饮食信息"
        }
    },
    "exercise_record": {
        "name": "运动记录",
        "keywords": [
            "运动", "锻炼", "健身", "跑步", "运动记录", "健身打卡", "体育",
            "散步", "游泳", "瑜伽", "骑车", "爬山", "球类", "运动计划",
            "训练", "减肥运动", "有氧", "无氧", "运动打卡"
        ],
        "high_priority_keywords": ["运动记录", "运动打卡", "健身打卡", "记录运动"],
        "negative_keywords": ["不想运动", "不愿意", "停止", "累了", "不动"],
        "action": {
            "type": "navigate",
            "url": "/pages/sport/sport",
            "title": "去记录运动",
            "icon": "💪",
            "description": "记录您的运动情况"
        }
    },
    "sleep_record": {
        "name": "睡眠记录",
        "keywords": [
            "睡眠", "睡觉", "休息", "失眠", "睡眠质量", "睡眠记录", "睡眠打卡",
            "入睡", "起床", "熬夜", "午睡", "睡眠时间", "睡眠习惯", "记录睡眠"
        ],
        "high_priority_keywords": ["睡眠记录", "睡眠打卡", "记录睡眠"],
        "negative_keywords": ["不睡", "不想睡", "睡不着但不记录"],
        "action": {
            "type": "navigate",
            "url": "/pages/sleep/sleep",
            "title": "去记录睡眠",
            "icon": "😴",
            "description": "记录您的睡眠信息"
        }
    },
    "health_data": {
        "name": "健康数据",
        "keywords": [
            "体重", "血压", "心率", "血糖", "体温", "身高", "BMI",
            "测量", "记录数据", "健康指标", "体检", "身体数据", "健康数据"
        ],
        "high_priority_keywords": ["记录数据", "健康数据", "身体数据", "测量"],
        "negative_keywords": ["不测", "不记录"],
        "action": {
            "type": "navigate",
            "url": "/pages/index/index",
            "title": "去记录身体数据",
            "icon": "📊",
            "description": "记录您的身体健康数据"
        }
    },
    "health_info": {
        "name": "健康信息",
        "keywords": [
            "健康信息", "疾病", "病史", "过敏", "用药", "症状", "不适",
            "健康状况", "医疗记录", "慢性病", "完善信息"
        ],
        "high_priority_keywords": ["健康信息", "完善信息", "医疗记录"],
        "negative_keywords": ["不想说", "隐私"],
        "action": {
            "type": "navigate",
            "url": "/pages/illnessinfo/illnessinfo",
            "title": "去完善健康信息",
            "icon": "🏥",
            "description": "完善您的健康信息"
        }
    },
    "manual_checkin": {
        "name": "手动打卡",
        "keywords": [
            "打卡", "签到", "记录", "手动", "手动打卡", "手动记录", "打卡记录"
        ],
        "high_priority_keywords": ["手动打卡", "打卡", "手动记录"],
        "negative_keywords": ["自动", "不打卡"],
        "action": {
            "type": "navigate",
            "url": "/pages/manual/manual",
            "title": "去手动打卡",
            "icon": "✅",
            "description": "进行手动打卡操作"
        }
    }
}


def has_negative_context(text: str, negative_keywords: List[str]) -> bool:
    """检查是否包含否定语境"""
    for keyword in negative_keywords:
        if keyword in text:
            return True
    return False


def calculate_match_score_improved(text: str, keywords: List[str], high_priority_keywords: List[str] = None) -> float:
    """
    改进的匹配分数计算
    - 如果包含高权重关键词，直接给高分
    - 普通关键词匹配给较低分数
    - 多个关键词匹配会累加分数
    """
    text_lower = text.lower()
    score = 0.0

    # 检查高权重关键词
    if high_priority_keywords:
        for keyword in high_priority_keywords:
            if keyword.lower() in text_lower:
                score += 0.8  # 高权重关键词直接给0.8分
                print(f"[DEBUG] 高权重关键词匹配: '{keyword}' in '{text}', 当前分数: {score}")
                return score  # 匹配到高权重关键词就直接返回

    # 检查普通关键词
    matched_keywords = []
    for keyword in keywords:
        if keyword.lower() in text_lower:
            matched_keywords.append(keyword)
            score += 0.3  # 每个普通关键词给0.3分

    if matched_keywords:
        print(f"[DEBUG] 普通关键词匹配: {matched_keywords} in '{text}', 分数: {score}")

    # 限制最高分数
    return min(score, 1.0)


def recognize_intent(question: str) -> Optional[Dict[str, Any]]:
    """
    识别用户问题中的意图 - 改进版本
    """
    if not question or len(question.strip()) < 2:
        return None

    question = question.strip()
    print(f"[DEBUG] 开始分析问题: '{question}'")

    best_intent = None
    best_score = 0
    threshold = 0.25  # 降低阈值

    # 分析每个意图
    for intent_id, intent_config in INTENT_RULES.items():
        print(f"[DEBUG] 检查意图: {intent_id} ({intent_config['name']})")

        # 检查否定语境
        if has_negative_context(question, intent_config["negative_keywords"]):
            print(f"[DEBUG] {intent_id} 被否定语境排除")
            continue

        # 计算匹配分数
        score = calculate_match_score_improved(
            question,
            intent_config["keywords"],
            intent_config.get("high_priority_keywords", [])
        )

        print(f"[DEBUG] {intent_id} 最终分数: {score}")

        if score > threshold and score > best_score:
            best_score = score
            best_intent = {
                "intent_id": intent_id,
                "intent_name": intent_config["name"],
                "confidence": score,
                "action": intent_config["action"]
            }
            print(f"[DEBUG] 更新最佳意图: {intent_id}, 分数: {score}")

    if best_intent:
        print(f"[DEBUG] 最终识别结果: {best_intent['intent_id']} (置信度: {best_intent['confidence']})")
    else:
        print(f"[DEBUG] 未识别到任何意图")

    return best_intent


def get_all_intents() -> Dict[str, Any]:
    """获取所有可用的意图配置"""
    return {
        "intents": {
            intent_id: {
                "name": config["name"],
                "action": config["action"]
            }
            for intent_id, config in INTENT_RULES.items()
        }
    }


# 简单的测试函数
def test_intent_recognition():
    """测试意图识别功能"""
    test_cases = [
        "我想记录今天的饮食",
        "今天吃了什么应该怎么记录",
        "饮食打卡",
        "我要去运动了",
        "运动记录",
        "睡眠质量不好，想记录一下",
        "记录睡眠",
        "我不想运动",
        "体重需要测量一下",
        "手动打卡",
        "想要打卡",
        "今天天气真好"
    ]

    print("=" * 50)
    print("意图识别测试")
    print("=" * 50)

    for case in test_cases:
        print(f"\n问题: {case}")
        result = recognize_intent(case)
        if result:
            print(f"✅ 识别到意图: {result['intent_name']} (置信度: {result['confidence']:.2f})")
            print(f"   操作: {result['action']['title']}")
        else:
            print("❌ 未识别到意图")
        print("-" * 30)


if __name__ == "__main__":
    test_intent_recognition()