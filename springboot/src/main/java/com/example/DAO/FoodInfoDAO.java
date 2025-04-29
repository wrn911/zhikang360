package com.example.DAO;
import com.fasterxml.jackson.annotation.JsonCreator;
import lombok.Data;

import java.util.List;

@Data // Lombok 注解
public class FoodInfoDAO {

    // 饮食偏好（合并前端预设选项和自定义输入）
    private List<String> preferences;

    // 忌口食物（合并前端预设选项和自定义输入）
    private List<String> avoids;

    // 饮食计划配合意愿（1-5级）
    private String willingness;
}
