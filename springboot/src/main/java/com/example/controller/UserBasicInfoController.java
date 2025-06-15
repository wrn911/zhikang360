package com.example.controller;

import com.example.DAO.FoodInfoDAO;
import com.example.DAO.IllnessInfoDAO;
import com.example.DAO.SleepInfoDAO;
import com.example.DAO.SportInfoDAO;
import com.example.common.Result;
import com.example.context.BaseContext;
import com.example.entity.*;
import com.example.service.PythonHealthSyncService;
import com.example.service.UserBasicInfoService;
import com.github.pagehelper.PageInfo;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import javax.annotation.Resource;

@RestController
@RequestMapping("/user-basic-info")
public class UserBasicInfoController {

    @Resource
    private UserBasicInfoService userBasicInfoService;
    @Autowired
    private PythonHealthSyncService pythonHealthSyncService;

    private static final Logger logger = LoggerFactory.getLogger(PythonHealthSyncService.class);


    @PostMapping("/food_info/add")
    public Result addFoodInfo(@RequestBody FoodInfoDAO foodInfoDAO) {
        userBasicInfoService.addFoodInfo(foodInfoDAO);
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

    @GetMapping("/recommend/select")
    public Result selectRecommend() {
        return Result.success(userBasicInfoService.selectRecommend());
    }

    @PutMapping("/food_info/update")
    public Result updateFoodInfoById(@RequestBody FoodInfo foodInfo) {
        userBasicInfoService.updateFoodInfoById(foodInfo);
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

    @GetMapping("/food_info/selectById")
    public Result selectFoodInfoById() {
        return Result.success(userBasicInfoService.selectFoodInfoById());
    }

    @PostMapping("/sport_info/add")
    public Result addSportInfo(@RequestBody SportInfoDAO sportInfoDAO) {
        userBasicInfoService.addSportInfo(sportInfoDAO);
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

    @PutMapping("/sport_info/update")
    public Result updateSportInfoById(@RequestBody SportInfo sportInfo) {
        userBasicInfoService.updateSportInfoById(sportInfo);
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

    @GetMapping("/sport_info/selectById")
    public Result selectSportInfoById() {
        return Result.success(userBasicInfoService.selectSportInfoById());
    }

    @PostMapping("/sleep_info/add")
    public Result addSleepInfo(@RequestBody SleepInfoDAO sleepInfoDAO) {
        userBasicInfoService.addSleepInfo(sleepInfoDAO);
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

    @PutMapping("/sleep_info/update")
    public Result updateSleepInfoById(@RequestBody SleepInfo sleepInfo) {
        userBasicInfoService.updateSleepInfoById(sleepInfo);
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

    @GetMapping("/sleep_info/selectById")
    public Result selectSleepInfoById() {
        return Result.success(userBasicInfoService.selectSleepInfoById());
    }

    @PostMapping("/illness_info/add")
    public Result addIllnessInfo(@RequestBody IllnessInfoDAO illnessInfoDAO) {
        userBasicInfoService.addIllnessInfo(illnessInfoDAO);
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

    @PutMapping("/illness_info/update")
    public Result updateIllnessInfoById(@RequestBody IllnessInfo illnessInfo) {
        userBasicInfoService.updateIllnessInfoById(illnessInfo);
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

    @GetMapping("/illness_info/selectById")
    public Result selectIllnessInfoById() {
        return Result.success(userBasicInfoService.selectIllnessInfoById());
    }

    @PostMapping("/add")
    public Result add(@RequestBody UserBasicInfo userBasicInfo) {
        userBasicInfoService.add(userBasicInfo);
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

    @DeleteMapping("/delete/{userId}")
    public Result deleteById(@PathVariable Integer userId) {
        userBasicInfoService.deleteById(userId);
        return Result.success();
    }

    @PutMapping("/update")
    public Result updateById(@RequestBody UserBasicInfo userBasicInfo) {
        userBasicInfoService.updateById(userBasicInfo);
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

    @GetMapping("/selectById/{userId}")
    public Result selectById(@PathVariable Integer userId) {
        return Result.success(userBasicInfoService.selectById(userId));
    }

    @GetMapping("/selectPage")
    public Result selectPage(UserBasicInfo condition,
                             @RequestParam(defaultValue = "1") Integer pageNum,
                             @RequestParam(defaultValue = "10") Integer pageSize) {
        PageInfo<UserBasicInfo> page = userBasicInfoService.selectPage(condition, pageNum, pageSize);
        return Result.success(page);
    }

}
