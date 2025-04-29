package com.example.entity;

import lombok.Data;
import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Date;
import java.time.LocalDateTime;

@Data
public class UserBasicInfo implements Serializable {
    private static final long serialVersionUID = 1L;

    private Long userId;
    private String gender;
    private Date birthDate;
    private double height;
    private double weight;
    private String bloodPressure;
    private double bloodSugar;
    private LocalDateTime updateTimeH;
    private LocalDateTime updateTimeW;
    private LocalDateTime updateTimeBp;
    private LocalDateTime updateTimeBs;
}
