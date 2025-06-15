package com.example.mapper;

import com.example.DAO.CheckinCountDTO;
import com.example.entity.*;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.time.LocalDate;
import java.util.Date;
import java.util.List;
import java.util.Map;

/**
 * 操作 exercise 表相关数据接口
 */
public interface ExerciseCheckinMapper {

    /**
     * 根据用户Id查询历史运动
     */
    @Select("select * from exercise_checkin where user_id = #{userId}")
    List<ExerciseCheckin> selectHistory(Long userId);

    /**
     * 新增
     */
    int insertBatch(List<Map> list);

    /**
     * 根据时间查询
     */
    List<ExerciseCheckin> selectByTime(Date begin, Date end);

    /**
     * 查询所有（可带简单条件）
     */
    List<ExerciseCheckin> selectAll(Map map);

    /**
     * 根据ID查询
     */
    ExerciseCheckin selectById(Long id);

    /**
     * 删除
     */
    int deleteById(Integer id);

    /**
     * 修改
     */
    int updateById(ExerciseCheckin exerciseCheckin);

    CheckinCountDTO selectCheckinCounts(Long userId);

    List<UserExerciseRecommendList> selectByCategory(@Param("userId") Long userId, @Param("exercise_category") String type);

    List<UserExerciseRecommendList> selectTodayRecommendedExercises(@Param("userId") Long userId, @Param("today") LocalDate today);

    List<ExerciseCheckin> selectByUserIdAndDate(@Param("userId") Long userId,
                                              @Param("date") String date);
    List<ExerciseCheckin> selectTodayUncheckinByUser(@Param("userId") Long userId, @Param("today") LocalDate today);

    void insert(ExerciseCheckin record);

    void insertUserExerciseRecommendFromTemplate(@Param("userId") Long userId);

    UserExerciseRecommendList selectUserExerciseRecommendListById(@Param("id") Integer id);

    void updateWeight(@Param("id") Integer id,
                      @Param("weight") Double weight);


}

