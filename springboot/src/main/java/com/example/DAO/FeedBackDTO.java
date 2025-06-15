package com.example.DAO;

import java.util.List;

// userId这里没提供，可以用Long userId = BaseContext.getCurrentId()在后端获得userId

public class FeedBackDTO {
    private List<FoodFeedBackDTO> foodFeedbackList;
    private List<ExerciseFeedBackDTO> exerciseFeedbackList;

    public List<FoodFeedBackDTO> getFoodFeedbackList() {
        return foodFeedbackList;
    }

    public void setFoodFeedbackList(List<FoodFeedBackDTO> foodFeedbackList) {
        this.foodFeedbackList = foodFeedbackList;
    }

    public List<ExerciseFeedBackDTO> getExerciseFeedbackList() {
        return exerciseFeedbackList;
    }

    public void setExerciseFeedbackList(List<ExerciseFeedBackDTO> exerciseFeedbackList) {
        this.exerciseFeedbackList = exerciseFeedbackList;
    }
}

