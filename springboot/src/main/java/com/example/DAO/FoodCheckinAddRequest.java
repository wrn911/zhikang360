package com.example.DAO;

import com.fasterxml.jackson.annotation.JsonCreator;
import lombok.Data;

@Data
public class FoodCheckinAddRequest {
    // 食物ID（根据业务需求决定是否允许空值）
    private Integer foodId;

    // 食物名称（前端展示用）
    private String foodName;

    // 食物分类
    private String category;

    // 摄入克数（取整后）
    private Integer grams;

    // 餐别类型（枚举校验）
    private MealType mealType;


    // 定义餐别枚举
    public enum MealType {
        BREAKFAST("早餐"),
        LUNCH("午餐"),
        DINNER("晚餐"),
        OTHER("其他");

        private final String chineseName;

        MealType(String chineseName) {
            this.chineseName = chineseName;
        }

        // 获取中文显示名称
        public String getChineseName() {
            return chineseName;
        }

        // JSON反序列化方法
        @JsonCreator
        public static MealType fromChinese(String chinese) {
            for (MealType type : values()) {
                if (type.chineseName.equals(chinese)) {
                    return type;
                }
            }
            return OTHER;
        }
    }
}