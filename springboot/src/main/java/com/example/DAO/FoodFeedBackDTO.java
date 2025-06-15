package com.example.DAO;

public class FoodFeedBackDTO {
    private Integer foodRecommendListId;
    private int feedback;

    public Integer getFoodRecommendListId() {
        return foodRecommendListId;
    }

    public void setFoodRecommendListId(Integer foodRecommendListId) {
        this.foodRecommendListId = foodRecommendListId;
    }

    public int getFeedback() {
        return feedback;
    }

    public void setFeedback(int feedback) {
        this.feedback = feedback;
    }
}
