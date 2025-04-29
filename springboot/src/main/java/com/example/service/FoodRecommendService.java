package com.example.service;

import com.example.context.BaseContext;
import com.example.entity.*;
import com.example.DAO.FoodCheckinAddRequest;
import com.example.DAO.FoodCheckinStatsDAO;
import java.time.format.DateTimeFormatter;
import com.example.mapper.FoodMapper;
import com.example.mapper.FoodRecommendMapper;
import java.time.YearMonth;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class FoodRecommendService {
    private static final float TARGET_CALORIES = 800.0f;

    @Autowired
    private FoodMapper foodMapper;

    @Autowired
    private FoodRecommendMapper foodRecommendMapper;

    public Map<String, ArrayList<FoodRecommend>> simpleSelect() {
        Long userId = BaseContext.getCurrentId();
        LocalDate today = LocalDate.now();
        String date = today.toString();
        List<FoodRecommend> foodRecommends = foodRecommendMapper.selectByUserIdAndDate(userId, date);
        if(foodRecommends.isEmpty()){
            this.recommend(userId);
        }
        Map<String, ArrayList<FoodRecommend>> foodRecommendMap = new HashMap<>();
        //格式：食物类型：【相关食物】
        for (FoodRecommend foodRecommend : foodRecommends) {
            if (!foodRecommendMap.containsKey(foodRecommend.getRecommendType())) {
                foodRecommendMap.put(foodRecommend.getRecommendType(), new ArrayList<>());
            }
            foodRecommendMap.get(foodRecommend.getRecommendType()).add(foodRecommend);
        }
        return foodRecommendMap;
    }
    @Transactional
    public void recommend(Long userId) {
        List<Food> allFoods = foodMapper.selectAll(new Food());
        this.recommendFoods(TARGET_CALORIES, allFoods, "早餐", userId);
        this.recommendFoods(TARGET_CALORIES, allFoods, "午餐", userId);
        this.recommendFoods(TARGET_CALORIES, allFoods, "晚餐", userId);
    }

    public void recommendFoods(float targetCalories, List<Food> allFoods, String type, Long userId) {
        Collections.shuffle(allFoods);//打乱列表，引入随机性
        Double totalCalories = 0.0;
        float everCalories = targetCalories / 3.0f;
        for (Food food : allFoods) {
            if (food.getCalories() <= everCalories) {
                FoodRecommend foodRecommend = new FoodRecommend();
                foodRecommend.setUserId(userId);
                foodRecommend.setFoodId(food.getId());
                foodRecommend.setFoodName(food.getName());
                foodRecommend.setRecommendType(type);
                Integer grams = Math.round(everCalories / food.getCalories()) * 100;
                foodRecommend.setGramAte(grams);
                Double b = (double)grams / 100;
                foodRecommend.setCaloriesAte(Math.round(food.getCalories() * b * 10) / 10.0);
                foodRecommend.setCarbohydratesAte(Math.round(food.getCarbohydrates() * b * 10) / 10.0);
                foodRecommend.setFatAte(Math.round(food.getFat() * b * 10) / 10.0);
                foodRecommend.setProteinAte(Math.round(food.getProtein() * b * 10) / 10.0);
                foodRecommend.setFiberAte(Math.round(food.getFiber() * b * 10) / 10.0);
                foodRecommend.setCreateTime(LocalDateTime.now());
                totalCalories += foodRecommend.getCaloriesAte();
                foodRecommendMapper.insert(foodRecommend);
                // 如果已达到目标卡路里消耗，停止推荐
                if (totalCalories >= targetCalories*0.95) {
                    break;
                }
            }
        }
    }
}
