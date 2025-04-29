package com.example.entity;

import lombok.Data;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * 运动实体类，对应数据库中的 exercise 表
 */
@Data
public class FoodRecommend implements Serializable {
    private static final long serialVersionUID = 1L;

    private Integer recommendId;         // 主键
    private Long userId;            // 用户ID（外键）
    private String recommendType;        // 餐别（早/午/晚餐）
    private Integer foodId;            // 食物ID（关联食物表）
    private String foodName;           // 食物名称
    private Integer gramAte;           // 摄入克数
    private Double caloriesAte;       // 摄入卡路里
    private Double carbohydratesAte;  // 摄入碳水
    private Double fatAte;            // 摄入脂肪
    private Double proteinAte;        // 摄入蛋白质
    private Double fiberAte;          // 摄入纤维素
    private LocalDateTime createTime;  // 创建时间
}
