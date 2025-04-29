package com.example.mapper;

import com.example.DAO.CheckinCountDTO;
import com.example.entity.FoodCheckin;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.time.LocalDate;
import java.util.List;

public interface FoodCheckinMapper {
    int insert(FoodCheckin foodCheckin);
    int deleteById(Integer checkinId);
    int updateById(FoodCheckin foodCheckin);
    FoodCheckin selectById(Integer checkinId);
    FoodCheckin selectByUserIdAndFoodId(@Param("userId") Long userId, @Param("foodId") Integer foodId, @Param("checkInType") String checkInType, @Param("date")LocalDate today);
    List<FoodCheckin> selectAll(FoodCheckin condition);
    List<FoodCheckin> selectHistory(@Param("userId") Long userId, @Param("date") String date);
    // 统计当天和前一天的打卡条数
    CheckinCountDTO selectCheckinCounts(@Param("userId") Long userId);

    // 统计打卡天数（去重后的日期数量）
    @Select("SELECT COUNT(DISTINCT DATE(create_time)) " +
            "FROM food_checkin " +
            "WHERE user_id = #{userId} " +
            "AND DATE_FORMAT(create_time, '%Y-%m') = #{month}")
    Integer countCheckinDays(@Param("month") String month, @Param("userId") Long userId);

    // 统计总摄入热量
    @Select("SELECT COALESCE(SUM(calories_ate), 0) " +
            "FROM food_checkin " +
            "WHERE user_id = #{userId} " +
            "AND DATE_FORMAT(create_time, '%Y-%m') = #{month}")
    Double sumCalories(@Param("month") String month, @Param("userId") Long userId);
}
