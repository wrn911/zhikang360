package com.example.entity;
import lombok.Data;

import java.time.LocalDateTime;

@Data
public class SleepInfo {
    private Integer id;
    private Long userId;
    private String sleepTime;
    private String wakeupTime;
    private String emotions;
    private LocalDateTime createTime;
    private LocalDateTime updateTime;
}