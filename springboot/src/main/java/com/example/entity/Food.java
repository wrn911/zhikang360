package com.example.entity;

import java.io.Serializable;

/**
 * 食物实体类，对应数据库中的 food 表
 */
public class Food implements Serializable {
    private static final long serialVersionUID = 1L;

    private Integer id;             // 主键ID
    private String name;            // 食物名称
    private String category;        // 食物类别
    private Integer calories;       // 卡路里
    private Double carbohydrates;   // 碳水化合物
    private Double fat;             // 脂肪
    private Double protein;         // 蛋白质
    private Double fiber;           // 纤维素
    private String unit;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public Integer getCalories() {
        return calories;
    }

    public void setCalories(Integer calories) {
        this.calories = calories;
    }

    public Double getCarbohydrates() {
        return carbohydrates;
    }

    public void setCarbohydrates(Double carbohydrates) {
        this.carbohydrates = carbohydrates;
    }

    public Double getFat() {
        return fat;
    }

    public void setFat(Double fat) {
        this.fat = fat;
    }

    public Double getProtein() {
        return protein;
    }

    public void setProtein(Double protein) {
        this.protein = protein;
    }

    public Double getFiber() {
        return fiber;
    }

    public void setFiber(Double fiber) {
        this.fiber = fiber;
    }

    public String getUnit() {
        return unit;
    }

    public void setUnit(String unit) {
        this.unit = unit;
    }
}

