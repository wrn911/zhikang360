package com.example.entity;

import lombok.Data;

import java.io.Serializable;
@Data
public class UserFoodRecommendList implements Serializable {
    private static final long serialVersionUID = 1L;

    private Integer id;
    private Integer userId;
    private Integer foodRecommendListId;
    private String aim;
    private String grocery;
    private String time;
    private Integer foodId;
    private String foodName;
    private Double weight;
}

