package com.example.controller;

import com.example.common.Result;
import com.example.context.BaseContext;
import com.example.entity.Exercise;
import com.example.entity.ExerciseCheckin;
import com.example.entity.ExerciseRecommend;
import com.example.entity.FoodRecommend;
import com.example.mapper.ExerciseCheckinMapper;
import com.example.mapper.ExerciseMapper;
import com.example.service.ExerciseService;
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

/**
 * 运动信息前端操作接口
 */
@RestController
@RequestMapping("/exercise")
public class ExerciseController {

    @Autowired
    private ExerciseService exerciseService;

    @Autowired
    private ExerciseCheckinMapper exerciseCheckinMapper;

    @Autowired
    private PythonHealthSyncService pythonHealthSyncService;

    private static final Logger logger = LoggerFactory.getLogger(PythonHealthSyncService.class);

    /**
     * 获取运动列表
     */
    @GetMapping("/list")
    public Result simpleSelect() {
        Map<String, ArrayList<Exercise>> exerciseMap = exerciseService.simpleSelect();
        return Result.success(exerciseMap);
    }

    /**
     * 获取今日推荐运动
     */
    @GetMapping("/recommend")
    public Result selectRecommend(@RequestParam Integer expectedCalories) {
        List<ExerciseCheckin> recommendExercises = exerciseService.selectRecommend(expectedCalories);
        return Result.success(recommendExercises);
    }

    @PostMapping("/generate_recommend")
    public Result generateRecommend() {
        Long userId = BaseContext.getCurrentId();
        LocalDate today = LocalDate.now();
        String date = today.toString();
        List<ExerciseCheckin> exerciseCheckins = exerciseCheckinMapper.selectByUserIdAndDate(userId, date);
        if (exerciseCheckins.size() >= 3) {
            return Result.error("400", "目前已有三个及以上的推荐或自选，请勿重复操作");
        }
        exerciseService.generateRecommend();
        return Result.success();
    }

    /**
     * 打卡
     */
    @GetMapping("/checkin")
    public Result checkin(@RequestParam Integer checkinId, @RequestParam Integer feedback) {
        exerciseService.checkin(checkinId, feedback);
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

    /**
     * 在今日运动计划中添加新的运动
     */
    @PostMapping("/addNewToday")
    public Result addNewToday(@RequestBody ExerciseRecommend exercise) {
        exerciseService.addNewToday(exercise);
        return Result.success();
    }

    /**
     * 获取历史运动(按月份)
     */
    @GetMapping("/history")
    public Result selectHistory(@RequestParam String month) {
        Map<String, ArrayList<ExerciseCheckin>> exerciseCheckinMap = exerciseService.selectHistory(month);
        return Result.success(exerciseCheckinMap);
    }

    /**
     * 新增
     */
    @PostMapping("/add")
    public Result add(@RequestBody Exercise exercise) {
        exerciseService.add(exercise);
        return Result.success();
    }

    /**
     * 删除
     */
    @DeleteMapping("/delete/{id}")
    public Result deleteById(@PathVariable Integer id) {
        exerciseService.deleteById(id);
        return Result.success();
    }

    /**
     * 批量删除
     */
    @DeleteMapping("/delete/batch")
    public Result deleteBatch(@RequestBody List<Integer> ids) {
        exerciseService.deleteBatch(ids);
        return Result.success();
    }

    /**
     * 修改
     */
    @PutMapping("/update")
    public Result updateById(@RequestBody Exercise exercise) {
        exerciseService.updateById(exercise);
        return Result.success();
    }

    /**
     * 根据ID查询
     */
    @GetMapping("/selectById/{id}")
    public Result selectById(@PathVariable Integer id) {
        Exercise exercise = exerciseService.selectById(id);
        return Result.success(exercise);
    }

    /**
     * 查询所有
     */
    @GetMapping("/selectAll")
    public Result selectAll(Exercise exercise) {
        List<Exercise> list = exerciseService.selectAll(exercise);
        return Result.success(list);
    }

    /**
     * 分页查询
     */
    @GetMapping("/selectPage")
    public Result selectPage(Exercise exercise,
                             @RequestParam(defaultValue = "1") Integer pageNum,
                             @RequestParam(defaultValue = "10") Integer pageSize) {
        PageInfo<Exercise> page = exerciseService.selectPage(exercise, pageNum, pageSize);
        return Result.success(page);
    }
}