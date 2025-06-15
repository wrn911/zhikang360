package com.example.entity;

import lombok.Data;

import java.io.Serializable;
@Data
public class UserExerciseRecommendList implements Serializable {
    private static final long serialVersionUID = 1L;

    private Integer id;
    private Integer userId;
    private Integer exerciseRecommendListId;
    private Integer exerciseId;
    private String exerciseName;
    private String exerciseCategory;
    private String caloriesBurnRate;
    private Double weight;
}

