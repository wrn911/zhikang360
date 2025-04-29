package com.example.entity;

import lombok.Data;

import java.io.Serializable;

/**
 * 运动实体类，对应数据库中的 exercise 表
 */
@Data
public class Exercise implements Serializable {
    private static final long serialVersionUID = 1L;

    private Integer exerciseId;        // 主键ID
    private String exerciseName;       // 运动名称
    private String exerciseCategory;   // 运动类别
    private Integer caloriesBurnRate;  // 单位时间内消耗的热量
}