package com.example.DAO;

import com.fasterxml.jackson.annotation.JsonCreator;
import lombok.Data;

@Data
public class FoodCheckinStatsDAO  {
    // 当月打卡天数
    private Integer checkinDays;

    // 当月使用卡路里
    private Double finalCalories;

    // 当天
    private String selectedDate;

    //当月天数
    private Integer totalDays;

}
