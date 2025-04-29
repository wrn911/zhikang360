/**
package com.example.utils;
import java.util.*;
import com.example.entity.Exercise;
import com.example.entity.ExerciseRecommend;

public class ExerciseRecommendation {
    private final List<Exercise> exercises; // 所有可选运动列表

    public ExerciseRecommendation(List<Exercise> exercises) {
        this.exercises = exercises;
    }


     * 推荐运动组合，使总消耗接近预期卡路里
     * @param expectedCalories 用户预期消耗的卡路里
     * @return 推荐的运动列表（包含运动ID、名称、持续时长）

    public List<ExerciseRecommend> recommendExercises(int expectedCalories) {
        List<ExerciseRecommend> recommendations = new ArrayList<>();
        int remainingCalories = expectedCalories;

        // 按卡路里消耗率从高到低排序（优先推荐高效运动）
        List<Exercise> sortedExercises = new ArrayList<>(exercises);
        sortedExercises.sort(Comparator.comparingInt(Exercise::getCaloriesBurnRate).reversed());

        // 贪心算法：选择高消耗率的运动，逐步逼近目标
        for (Exercise exercise : sortedExercises) {
            if (remainingCalories <= 0) break;

            // 计算该运动最大可持续时长（以10分钟为单位，避免小数）
            int maxDuration = (remainingCalories * 10) / exercise.getCaloriesBurnRate();
            if (maxDuration <= 0) continue;

            // 随机生成一个合理时长（防止全部用最大时长）
            int duration = Math.min(maxDuration, new Random().nextInt(maxDuration) + 1);
            int calories = (duration * exercise.getCaloriesBurnRate()) / 10;

            // 记录推荐
            recommendations.add(new ExerciseRecommend(
                    exercise.getExerciseId(),
                    exercise.getExerciseName(),
                    duration,
                    exercise.getCaloriesBurnRate()
            ));
            remainingCalories -= calories;
        }

        // 如果仍有剩余卡路里，补充一个随机运动
        if (remainingCalories > 0 && !sortedExercises.isEmpty()) {
            Exercise randomExercise = sortedExercises.get(new Random().nextInt(sortedExercises.size()));
            int duration = (remainingCalories * 10) / randomExercise.getCaloriesBurnRate();
            if (duration > 0) {
                recommendations.add(new ExerciseRecommend(
                        randomExercise.getExerciseId(),
                        randomExercise.getExerciseName(),
                        duration,
                        randomExercise.getCaloriesBurnRate()
                ));
            }
        }

        return recommendations;
    }
}*/
package com.example.utils;

import com.example.entity.Exercise;
import com.example.entity.ExerciseCheckin;
import com.example.entity.ExerciseRecommend;
import org.springframework.beans.BeanUtils;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class ExerciseRecommendation {

    private List<Exercise> exerciseList;

    public ExerciseRecommendation(List<Exercise> exerciseList) {
        this.exerciseList = exerciseList;
    }

    public List<ExerciseRecommend> recommendExercises(int targetCalories) {
        List<ExerciseRecommend> recommendedExercises = new ArrayList<>();
        Collections.shuffle(recommendedExercises);//打乱列表，引入随机性

        int totalCalories = 0;
        int everCalories = targetCalories / 3;
        for (Exercise exercise : exerciseList) {
            if (exercise.getCaloriesBurnRate() <= everCalories) {
                ExerciseRecommend exerciseRecommend = new ExerciseRecommend();
                BeanUtils.copyProperties(exercise, exerciseRecommend);
                exerciseRecommend.setCalories((everCalories / exercise.getCaloriesBurnRate()) * exercise.getCaloriesBurnRate());
                exerciseRecommend.setDuration(everCalories / exercise.getCaloriesBurnRate() * 10);
                recommendedExercises.add(exerciseRecommend);
                totalCalories += exerciseRecommend.getCalories();

                // 如果已达到目标卡路里消耗，停止推荐
                if (totalCalories >= targetCalories) {
                    break;
                }
            }
        }

        return recommendedExercises;
    }
}
