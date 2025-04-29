package com.example.entity;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Date;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class UserCheckInfo {
    private Long userId;
    private Integer foodAddDay;
    private Integer sportAddDay;
    private Integer foodContinueDay;
    private Integer sportContinueDay;
    private Double addFoodCal;
    private Double addSportCal;
}
