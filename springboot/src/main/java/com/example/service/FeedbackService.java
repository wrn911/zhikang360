package com.example.service;

import com.example.DAO.ExerciseFeedBackDTO;
import com.example.DAO.FeedBackDTO;
import com.example.DAO.FoodFeedBackDTO;
import com.example.context.BaseContext;
import com.example.entity.Feedback;
import com.example.entity.UserExerciseRecommendList;
import com.example.entity.UserFoodRecommendList;
import com.example.mapper.ExerciseCheckinMapper;
import com.example.mapper.FeedbackMapper;
import com.example.mapper.FoodRecommendMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

@Service
public class FeedbackService {
    private final FeedbackMapper mapper;

    @Autowired
    private FoodRecommendMapper foodRecommendMapper;

    @Autowired
    private ExerciseCheckinMapper exerciseCheckinMapper;


    public FeedbackService(FeedbackMapper mapper) {
        this.mapper = mapper;
    }

    public void addFeedback(FeedBackDTO feedbackDTO) {
        Feedback feedback = new Feedback();
        feedback.setUserId(BaseContext.getCurrentId());
        int foodNumber = 0;
        int sportNumber = 0;
        feedback.setPublishTime(LocalDateTime.now());
        for (FoodFeedBackDTO foodDTO : feedbackDTO.getFoodFeedbackList()) {
            foodNumber = foodNumber * 10 + foodDTO.getFeedback();
        }
        for (ExerciseFeedBackDTO exerciseFeedBackDTO : feedbackDTO.getExerciseFeedbackList()) {
            sportNumber = sportNumber * 10 + exerciseFeedBackDTO.getFeedback();
        }
        feedback.setFoodNumber(foodNumber);
        feedback.setSportNumber(sportNumber);
        mapper.insert(feedback);
    }

    public Feedback getByUserAndDate(Long userId, LocalDate date) {
        return mapper.selectByUserIdAndDate(userId, date);
    }

    public List<Feedback> listByUserId(Long userId) {
        return mapper.selectAllByUserId(userId);
    }

    public void deleteById(int id) {
        mapper.deleteById(id);
    }

    public void updateFeedback(Feedback feedback) {
        mapper.update(feedback);
    }

    @Transactional
    public void updateFoodFeedback(Long userId, Integer id, int feedback) {
        // 1. 根据主键id查找当前记录
        UserFoodRecommendList userFoodRecommendList = foodRecommendMapper.selectUserFoodRecommendListById(id);

        // 2. 获取当前记录的time和userId
        String time = userFoodRecommendList.getTime();
        String aim = userFoodRecommendList.getAim();
        String grocery = userFoodRecommendList.getGrocery();

        // 3. 获取同一用户同一时间的所有记录
        List<UserFoodRecommendList> userFoodRecommendLists = foodRecommendMapper.selectByAimAndGroceryAndTime(userId, aim, grocery, time);

        // 4. 计算权重变化
        double weightChange = 0.0;
        switch (feedback) {
            case 3: weightChange = 0.5 * userFoodRecommendList.getWeight(); break; // 满意
            case 2: weightChange = 0.0; break; // 尚可
            case 1: weightChange = -0.5 * userFoodRecommendList.getWeight(); break; // 不满意
        }
        if(feedback != 2){
            // 5. 更新当前记录的权重
            double newWeight = Math.max(0.01, userFoodRecommendList.getWeight() + weightChange);
            foodRecommendMapper.updateWeight(userFoodRecommendList.getId(), newWeight);

            // 6. 重新计算所有记录的总权重
            double totalWeight = userFoodRecommendLists.stream()
                    .mapToDouble(fb -> fb.getId().equals(id) ? newWeight : fb.getWeight())
                    .sum();

            // 7. 如果总权重不为1，调整其他记录的权重
            if (Math.abs(totalWeight - 1.0) > 0.0001 && userFoodRecommendLists.size() > 1) {
                double remain = 1.0 - newWeight;
                double sumOther = userFoodRecommendLists.stream()
                        .filter(fb -> !fb.getId().equals(id))
                        .mapToDouble(UserFoodRecommendList::getWeight)
                        .sum();
                for (UserFoodRecommendList fb : userFoodRecommendLists) {
                    if (!fb.getId().equals(id)) {
                        double adjustedWeight = Math.max(0.01, fb.getWeight() * remain / (sumOther == 0 ? 1 : sumOther));
                        foodRecommendMapper.updateWeight(fb.getId(), adjustedWeight);
                    }
                }
            }
        }
    }

    @Transactional
    public void updateExerciseFeedback(Long userId, Integer id, int feedback) {
        // 1. 根据主键id查找当前记录
        UserExerciseRecommendList userExerciseRecommendList = exerciseCheckinMapper.selectUserExerciseRecommendListById(id);

        // 2. 获取当前记录的time和userId
        String category = userExerciseRecommendList.getExerciseCategory();

        // 3. 获取同一用户同一时间的所有记录
        List<UserExerciseRecommendList> userExerciseRecommendLists = exerciseCheckinMapper.selectByCategory(userId, category);

        // 4. 计算权重变化
        double weightChange = 0.0;
        switch (feedback) {
            case 3: weightChange = 0.5 * userExerciseRecommendList.getWeight(); break; // 满意
            case 2: weightChange = 0.0; break; // 尚可
            case 1: weightChange = -0.5 * userExerciseRecommendList.getWeight(); break; // 不满意
        }
        if(feedback != 2){
            // 5. 更新当前记录的权重
            double newWeight = Math.max(0.01, userExerciseRecommendList.getWeight() + weightChange);
            exerciseCheckinMapper.updateWeight(userExerciseRecommendList.getId(), newWeight);

            // 6. 重新计算所有记录的总权重
            double totalWeight = userExerciseRecommendLists.stream()
                    .mapToDouble(fb -> fb.getId().equals(id) ? newWeight : fb.getWeight())
                    .sum();

            // 7. 如果总权重不为1，调整其他记录的权重
            if (Math.abs(totalWeight - 1.0) > 0.000001 && userExerciseRecommendLists.size() > 1) {
                double remain = 1.0 - newWeight;
                double sumOther = userExerciseRecommendLists.stream()
                        .filter(fb -> !fb.getId().equals(id))
                        .mapToDouble(UserExerciseRecommendList::getWeight)
                        .sum();
                for (UserExerciseRecommendList fb : userExerciseRecommendLists) {
                    if (!fb.getId().equals(id)) {
                        double adjustedWeight = Math.max(0.01, fb.getWeight() * remain / (sumOther == 0 ? 1 : sumOther));
                        exerciseCheckinMapper.updateWeight(fb.getId(), adjustedWeight);
                    }
                }
            }

        }
    }
}

