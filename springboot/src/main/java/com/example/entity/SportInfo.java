package com.example.entity;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.List;
@Data
public class SportInfo {
    private Integer id;
    private Long userId;
    private String preferences;
    private String weaknesses;
    private String experience;
    private String intensity;
    private String willingness;
    private String freeTimes;
    private LocalDateTime createTime;
    private LocalDateTime updateTime;
}
