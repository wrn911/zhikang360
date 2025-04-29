package com.example.controller;

import com.example.DAO.FoodInfoDAO;
import com.example.DAO.IllnessInfoDAO;
import com.example.DAO.SleepInfoDAO;
import com.example.DAO.SportInfoDAO;
import com.example.common.Result;
import com.example.entity.*;
import com.example.service.UserBasicInfoService;
import com.github.pagehelper.PageInfo;
import org.springframework.web.bind.annotation.*;
import javax.annotation.Resource;

@RestController
@RequestMapping("/user-basic-info")
public class UserBasicInfoController {

    @Resource
    private UserBasicInfoService userBasicInfoService;


    @PostMapping("/food_info/add")
    public Result addFoodInfo(@RequestBody FoodInfoDAO foodInfoDAO) {
        userBasicInfoService.addFoodInfo(foodInfoDAO);
        return Result.success();
    }

    @PutMapping("/food_info/update")
    public Result updateFoodInfoById(@RequestBody FoodInfo foodInfo) {
        userBasicInfoService.updateFoodInfoById(foodInfo);
        return Result.success();
    }

    @GetMapping("/food_info/selectById")
    public Result selectFoodInfoById() {
        return Result.success(userBasicInfoService.selectFoodInfoById());
    }

    @PostMapping("/sport_info/add")
    public Result addSportInfo(@RequestBody SportInfoDAO sportInfoDAO) {
        userBasicInfoService.addSportInfo(sportInfoDAO);
        return Result.success();
    }

    @PutMapping("/sport_info/update")
    public Result updateSportInfoById(@RequestBody SportInfo sportInfo) {
        userBasicInfoService.updateSportInfoById(sportInfo);
        return Result.success();
    }

    @GetMapping("/sport_info/selectById")
    public Result selectSportInfoById() {
        return Result.success(userBasicInfoService.selectSportInfoById());
    }

    @PostMapping("/sleep_info/add")
    public Result addSleepInfo(@RequestBody SleepInfoDAO sleepInfoDAO) {
        userBasicInfoService.addSleepInfo(sleepInfoDAO);
        return Result.success();
    }

    @PutMapping("/sleep_info/update")
    public Result updateSleepInfoById(@RequestBody SleepInfo sleepInfo) {
        userBasicInfoService.updateSleepInfoById(sleepInfo);
        return Result.success();
    }

    @GetMapping("/sleep_info/selectById")
    public Result selectSleepInfoById() {
        return Result.success(userBasicInfoService.selectSleepInfoById());
    }

    @PostMapping("/illness_info/add")
    public Result addIllnessInfo(@RequestBody IllnessInfoDAO illnessInfoDAO) {
        userBasicInfoService.addIllnessInfo(illnessInfoDAO);
        return Result.success();
    }

    @PutMapping("/illness_info/update")
    public Result updateIllnessInfoById(@RequestBody IllnessInfo illnessInfo) {
        userBasicInfoService.updateIllnessInfoById(illnessInfo);
        return Result.success();
    }

    @GetMapping("/illness_info/selectById")
    public Result selectIllnessInfoById() {
        return Result.success(userBasicInfoService.selectIllnessInfoById());
    }

    @PostMapping("/add")
    public Result add(@RequestBody UserBasicInfo userBasicInfo) {
        userBasicInfoService.add(userBasicInfo);
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
