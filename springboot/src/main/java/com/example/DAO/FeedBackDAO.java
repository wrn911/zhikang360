package com.example.DAO;

import com.example.entity.UserExerciseRecommendList;
import com.example.entity.UserFoodRecommendList;
import lombok.Data;

import java.util.List;
@Data
public class FeedBackDAO {
    private List<UserFoodRecommendList> foodFeedbackList;
    private List<UserExerciseRecommendList> exerciseFeedbackList;
}
