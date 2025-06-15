package com.example.controller;

import com.example.common.Result;
import com.example.context.BaseContext;
import com.example.entity.*;
import com.example.DAO.FoodCheckinAddRequest;
import com.example.DAO.FoodCheckinStatsDAO;
import com.example.mapper.FoodRecommendMapper;
import com.example.service.ExerciseService;
import com.example.service.FoodCheckinService;
import com.example.service.FoodRecommendService;
import com.example.service.PythonHealthSyncService;
import com.github.pagehelper.PageInfo;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.time.LocalDate;
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

    @Autowired
    private FoodRecommendMapper foodRecommendMapper;

    @Autowired
    private PythonHealthSyncService pythonHealthSyncService;

    private static final Logger logger = LoggerFactory.getLogger(PythonHealthSyncService.class);

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
        // 触发Python端知识库更新
        int userId = Math.toIntExact(BaseContext.getCurrentId());
        try {
            pythonHealthSyncService.syncUserHealthData(userId, false);
        } catch (Exception e) {
            // 即使同步失败也不影响主业务流程
            logger.warn("触发Python健康数据同步失败，用户ID: {}", userId);
        }
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

    @PostMapping("/get_recommend")
    public Result GetRecommend() {
        Long userId = BaseContext.getCurrentId();
        LocalDate today = LocalDate.now();
        String date = today.toString();
        List<FoodRecommend> foodRecommends = foodRecommendMapper.selectByUserIdAndDate(userId, date);
        if (foodRecommends != null && !foodRecommends.isEmpty()) {
            return Result.error("400", "今日已生成推荐，请勿重复操作");
        }
        foodRecommendService.recommend(userId);
        return Result.success();
    }
}
