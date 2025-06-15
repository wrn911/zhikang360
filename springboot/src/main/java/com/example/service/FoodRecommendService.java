package com.example.service;

import com.example.common.enums.FoodGroceryEnum;
import com.example.common.enums.FoodTimeEnum;
import com.example.context.BaseContext;
import com.example.entity.*;
import com.example.DAO.FoodCheckinAddRequest;
import com.example.DAO.FoodCheckinStatsDAO;
import java.time.format.DateTimeFormatter;

import com.example.mapper.FoodInfoMapper;
import com.example.mapper.FoodMapper;
import com.example.mapper.FoodRecommendMapper;
import java.time.YearMonth;

import com.example.mapper.UserRecommendInfoMapper;
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
import java.math.BigDecimal;
import java.math.RoundingMode;

@Service
public class FoodRecommendService {

    @Autowired
    private FoodMapper foodMapper;

    @Autowired
    private FoodRecommendMapper foodRecommendMapper;

    @Autowired
    private UserRecommendInfoMapper userRecommendInfoMapper;

    @Autowired
    private FoodInfoMapper foodInfoMapper;

    public Map<String, ArrayList<FoodRecommend>> simpleSelect() {
        Long userId = BaseContext.getCurrentId();
        LocalDate today = LocalDate.now();
        String date = today.toString();
        List<FoodRecommend> foodRecommends = foodRecommendMapper.selectByUserIdAndDate(userId, date);
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
        UserRecommendInfo userRecommendInfo = userRecommendInfoMapper.selectByUserId(userId);
        String aim = foodInfoMapper.selectByUserId(userId).getAim();
        int recommendCalories = userRecommendInfo.getFoodCalories();
        this.recommendFoods(FoodTimeEnum.早餐.name(), (int)(recommendCalories * 0.3), aim, userId);
        this.recommendFoods(FoodTimeEnum.午餐.name(), (int)(recommendCalories * 0.4), aim, userId);
        this.recommendFoods(FoodTimeEnum.晚餐.name(), (int)(recommendCalories * 0.3), aim, userId);
    }

    public void recommendFoods(String time, int calories, String aim, Long userId) {
        int zhushiTarget = (int) (calories * 0.4);
        int zhengcanTarget = (int) (calories * 0.4);
        int fushiTarget = (int) (calories * 0.2);

        List<UserFoodRecommendList> foodZhushi = foodRecommendMapper.selectByAimAndGroceryAndTime(userId, aim, FoodGroceryEnum.主食.name(), time);
        List<UserFoodRecommendList> foodZhengcan = foodRecommendMapper.selectByAimAndGroceryAndTime(userId, aim, FoodGroceryEnum.正餐.name(), time);
        List<UserFoodRecommendList> foodFushi = foodRecommendMapper.selectByAimAndGroceryAndTime(userId, aim, FoodGroceryEnum.辅食.name(), time);

        FoodRecommend recommendZhushi = buildRecommend(foodZhushi, zhushiTarget, userId, time);
        FoodRecommend recommendZhengcan = buildRecommend(foodZhengcan, zhengcanTarget, userId, time);
        FoodRecommend recommendFushi = buildRecommend(foodFushi, fushiTarget, userId, time);

        // 保存推荐，可调用 foodRecommendMapper.insert() 三次
        foodRecommendMapper.insert(recommendZhushi);
        foodRecommendMapper.insert(recommendZhengcan);
        foodRecommendMapper.insert(recommendFushi);

    }

    private FoodRecommend buildRecommend(List<UserFoodRecommendList> candidates, int targetCalories, Long userId, String time) {
        if (candidates == null || candidates.isEmpty()) return null;

        // 构建前缀和（轮盘赌）
        double totalWeight = candidates.stream().mapToDouble(UserFoodRecommendList::getWeight).sum();
        List<Double> cumulative = new ArrayList<>();
        double acc = 0;
        for (UserFoodRecommendList f : candidates) {
            acc += f.getWeight() / totalWeight;
            cumulative.add(acc);
        }

        double r = Math.random();
        int index = 0;
        while (index < cumulative.size() && r > cumulative.get(index)) index++;

        UserFoodRecommendList selected = candidates.get(Math.min(index, candidates.size() - 1));
        Food food = foodMapper.selectById(selected.getFoodId());
        if (food == null || food.getCalories() == 0) return null;

        double rawGrams = (targetCalories * 100.0) / food.getCalories();
        int grams = Math.max(50, Math.min(600, (int) (Math.round(rawGrams / 50.0) * 50)));

        FoodRecommend result = new FoodRecommend();
        result.setUserId(userId);
        result.setRecommendType(time);
        result.setFoodId(food.getId());
        result.setFoodName(food.getName());
        result.setGramAte(grams);  // 保证在 50~600 且为 50 的倍数

        result.setCaloriesAte(round(food.getCalories() * grams / 100.0));
        result.setCarbohydratesAte(round(food.getCarbohydrates() * grams / 100.0));
        result.setFatAte(round(food.getFat() * grams / 100.0));
        result.setProteinAte(round(food.getProtein() * grams / 100.0));
        result.setFiberAte(round(food.getFiber() * grams / 100.0));
        result.setCreateTime(LocalDateTime.now());

        return result;
    }

    private double round(double value) {
        return BigDecimal.valueOf(value)
                .setScale(2, RoundingMode.HALF_UP)
                .doubleValue();
    }

    public List<UserFoodRecommendList> GetUserFoodRecommendList(){
        Long userId = BaseContext.getCurrentId();
        LocalDate date = LocalDate.now();
        return foodRecommendMapper.selectTodayRecommendedFoods(userId, date);
    }



}
