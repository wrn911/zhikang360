package com.example.entity;

import java.time.LocalDateTime;
import lombok.Data;
@Data
public class FoodInfo {
    private Integer id;
    private Long userId;
    private String preferences;
    private String avoids;
    private String willingness;
    private LocalDateTime createTime;
    private LocalDateTime updateTime;
    private String aim;
}
