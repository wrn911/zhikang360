package com.example.entity;

import lombok.Data;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * 运动实体类，对应数据库中的 exercise 表
 */
@Data
public class FoodRecommendList implements Serializable {
    private static final long serialVersionUID = 1L;

    private Integer id;         // 主键
    private String aim;            // 用户ID（外键）
    private String grocery;        // 餐别（早/午/晚餐）
    private String time;           // 食物名称
    private Integer foodId;           // 摄入克数
    private String foodName;       // 摄入卡路里
    private Double weight;
}