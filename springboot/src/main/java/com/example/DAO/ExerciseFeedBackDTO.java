package com.example.DAO;

public class ExerciseFeedBackDTO {
    private Integer exerciseRecommendListId;
    private int feedback;

    public Integer getExerciseRecommendListId() {
        return exerciseRecommendListId;
    }

    public void setExerciseRecommendListId(Integer exerciseRecommendListId) {
        this.exerciseRecommendListId = exerciseRecommendListId;
    }

    public int getFeedback() {
        return feedback;
    }

    public void setFeedback(int feedback) {
        this.feedback = feedback;
    }
}
