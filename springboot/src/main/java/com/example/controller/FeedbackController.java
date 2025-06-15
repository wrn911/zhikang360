package com.example.controller;

import com.example.DAO.ExerciseFeedBackDTO;
import com.example.DAO.FeedBackDAO;
import com.example.DAO.FeedBackDTO;
import com.example.DAO.FoodFeedBackDTO;
import com.example.common.Result;
import com.example.context.BaseContext;
import com.example.entity.Feedback;
import com.example.entity.FoodCheckin;
import com.example.entity.UserExerciseRecommendList;
import com.example.entity.UserFoodRecommendList;
import com.example.service.ExerciseService;
import com.example.service.FeedbackService;
import com.example.service.FoodRecommendService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/feedback")
public class FeedbackController {

    @Autowired
    private FeedbackService service;

    @Autowired
    private FoodRecommendService foodRecommendService;

    @Autowired
    private ExerciseService exerciseService;

    public FeedbackController(FeedbackService service) {
        this.service = service;
    }

    @GetMapping("/select")
    public Result get() {
        Long userId = BaseContext.getCurrentId();
        LocalDate date = LocalDate.now();
        Feedback feedback = service.getByUserAndDate(userId, date);
        if(feedback == null){
            feedback = new Feedback();
        }
        return Result.success(feedback);
    }

    @GetMapping("/list")
    public List<Feedback> list(@RequestParam Long userId) {
        return service.listByUserId(userId);
    }

    @DeleteMapping("/delete/{id}")
    public Result delete(@PathVariable int id) {
        service.deleteById(id);
        return Result.success();
    }

    @PostMapping("/changeWeight")
    public Result addFeedback(@RequestBody FeedBackDTO feedbackDTO) {
        Long userId = BaseContext.getCurrentId();
        service.addFeedback(feedbackDTO);
        if (feedbackDTO.getFoodFeedbackList() != null) {
            for (FoodFeedBackDTO foodDTO : feedbackDTO.getFoodFeedbackList()) {
                service.updateFoodFeedback(userId, foodDTO.getFoodRecommendListId(), foodDTO.getFeedback());
            }
        }
        if (feedbackDTO.getExerciseFeedbackList() != null) {
            for (ExerciseFeedBackDTO exerciseFeedBackDTO : feedbackDTO.getExerciseFeedbackList()) {
                service.updateExerciseFeedback(userId, exerciseFeedBackDTO.getExerciseRecommendListId(), exerciseFeedBackDTO.getFeedback());
            }
        }
        return Result.success();
    }

    // 得到今天的饮食推荐的具体user_recommend_list的行
    @GetMapping("/get_user_recommend_list")
    public Result GetUserRecommendList() {
        List<UserFoodRecommendList> userFoodRecommendLists  = foodRecommendService.GetUserFoodRecommendList();
        List<UserExerciseRecommendList> userExerciseRecommendLists = exerciseService.GetUserExerciseRecommendList();
        FeedBackDAO feedBackDAO = new FeedBackDAO();
        feedBackDAO.setFoodFeedbackList(userFoodRecommendLists);
        feedBackDAO.setExerciseFeedbackList(userExerciseRecommendLists);
        return Result.success(feedBackDAO);
    }
}

