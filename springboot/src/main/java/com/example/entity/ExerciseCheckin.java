package com.example.entity;

import cn.hutool.core.date.DateTime;
import lombok.Data;

import java.io.Serializable;
import java.time.LocalDateTime;
import java.util.Date;

/**
 * 运动签到实体类，对应数据库中的 checkin 表
 */
@Data
public class ExerciseCheckin implements Serializable {
    private static final long serialVersionUID = 1L;

    private Integer checkinId;        // 签到ID
    private Integer userId;           // 用户ID
    private LocalDateTime checkinDate;         // 签到时间
    private Integer exerciseId;      // 运动id
    private String exerciseName;       // 运动名称
    private Integer duration;          // 运动时长（分钟）
    private Integer caloriesBurned;   // 消耗卡路里
    private Integer additionalInfo;    // 附加信息（如步数、组数、次数等）
    private LocalDateTime createTime;          // 创建时间
    private Integer feedback;          // 用户反馈：0~2，从轻松到疲惫
}
