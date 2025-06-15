package com.example.service;

import com.example.entity.Exercise;
import com.example.entity.ExerciseCheckin;
import com.example.entity.ExerciseRecommend;
import com.example.entity.UserExerciseRecommendList;
import com.github.pagehelper.PageInfo;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/*
 * 运动信息业务处理
 */
public interface ExerciseService {
    /**
     * 简单查询所有
     */
    Map<String, ArrayList<Exercise>> simpleSelect();

    /**
     * 获取历史运动(按月份)
     */
    Map<String, ArrayList<ExerciseCheckin>> selectHistory(String month);

    /**
     * 获取历史运动
     */
    List<ExerciseCheckin> selectRecommend(Integer expectedCalories);

    /**
     * 在今日运动计划中添加新的运动
     */
    void addNewToday(ExerciseRecommend exercise);

    void checkMedal(Double addCal);

    /**
     * 打卡
     */
    void checkin(Integer checkinId, Integer feedback);

    /**
     * 新增
     */
    void add(Exercise exercise);

    /**
     * 删除
     */
    void deleteById(Integer id);

    void generateRecommend();
    List<UserExerciseRecommendList> GetUserExerciseRecommendList();

    /**
     * 批量删除
     */
    void deleteBatch(List<Integer> ids);

    /**
     * 修改
     */
    void updateById(Exercise exercise);

    /**
     * 根据ID查询
     */
    Exercise selectById(Integer id);

    /**
     * 查询所有
     */
    List<Exercise> selectAll(Exercise exercise);

    /**
     * 分页查询
     */
    PageInfo<Exercise> selectPage(Exercise exercise, Integer pageNum, Integer pageSize);
}

