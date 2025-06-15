package com.example.entity;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class Feedback {
    private Integer id;
    private Long userId;
    private Integer foodNumber;
    private Integer sportNumber;
    private LocalDateTime publishTime;
}

