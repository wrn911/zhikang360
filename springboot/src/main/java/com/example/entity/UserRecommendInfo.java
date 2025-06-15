package com.example.entity;

import lombok.Data;
import java.io.Serializable;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.Date;

@Data
public class UserRecommendInfo implements Serializable {
    private Long userId;
    private Integer foodCalories;
    private Integer exerciseCalories;
    private LocalTime sleepTimeStart;
    private LocalTime sleepTimeEnd;
    private LocalTime sleepTimeInmid;
}
