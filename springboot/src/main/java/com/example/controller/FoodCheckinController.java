package com.example.controller;

import com.example.common.Result;
import com.example.entity.*;
import com.example.DAO.FoodCheckinAddRequest;
import com.example.DAO.FoodCheckinStatsDAO;
import com.example.service.ExerciseService;
import com.example.service.FoodCheckinService;
import com.example.service.FoodRecommendService;
import com.github.pagehelper.PageInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/foodCheckin")
public class FoodCheckinController {

    @Autowired
    private FoodCheckinService foodCheckinService;

    @Autowired
    private FoodRecommendService foodRecommendService;


    /**
     * 获取食物列表
     */
    @GetMapping("/list")
    public Result simpleSelect() {
        Map<String, ArrayList<Food>> foodMap = foodCheckinService.simpleSelect();
        return Result.success(foodMap);
    }

    /**
     * 获取食物打卡列表
     */
    @GetMapping("/list_checkIn")
    public Result simpleSelectCheckin() {
        Map<String, ArrayList<FoodCheckin>> foodCheckinMap = foodCheckinService.simpleSelectCheckin();
        return Result.success(foodCheckinMap);
    }

    /**
     * 获取打卡天数和摄入总卡路里
     */
    @GetMapping("/stat")
    public Result selectCheckinDaysAndCalories() {
        FoodCheckinStatsDAO foodCheckinStatsDAO = foodCheckinService.selectCheckinDaysAndCalories();
        return Result.success(foodCheckinStatsDAO);
    }

    /**
     * 获取打卡天数和摄入总卡路里
     */
    @GetMapping("/recommend")
    public Result Recommend() {
        Map<String, ArrayList<FoodRecommend>> foodRecommendMap = foodRecommendService.simpleSelect();
        return Result.success(foodRecommendMap);
    }

    @PostMapping("/add")
    public Result add(@RequestBody FoodCheckinAddRequest foodCheckinAddRequest) {
        foodCheckinService.add(foodCheckinAddRequest);
        return Result.success();
    }

    @DeleteMapping("/delete/{checkinId}")
    public Result deleteById(@PathVariable Integer checkinId) {
        foodCheckinService.deleteById(checkinId);
        return Result.success();
    }

    @PutMapping("/update")
    public Result updateById(@RequestBody FoodCheckin foodCheckin) {
        foodCheckinService.updateById(foodCheckin);
        return Result.success();
    }


    /**
     * 获取历史饮食(按天数)
     */
    @GetMapping("/history")
    public Result selectHistory(@RequestParam String selectedDate) {
        Map<String, ArrayList<FoodCheckin>> foodCheckinMap = foodCheckinService.selectHistory(selectedDate);
        return Result.success(foodCheckinMap);
    }
}
