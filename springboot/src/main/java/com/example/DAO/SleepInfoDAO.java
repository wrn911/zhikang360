package com.example.DAO;

import lombok.Data;

import java.util.List;
@Data
public class SleepInfoDAO {
    // 睡眠时间
    private String sleepTime;

    // 起床时间
    private String wakeupTime;

    // 情绪选择
    private List<String> emotions;
}
