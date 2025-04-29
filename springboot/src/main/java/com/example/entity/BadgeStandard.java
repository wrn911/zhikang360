package com.example.entity;

import lombok.Data;
import java.io.Serializable;

@Data
public class BadgeStandard implements Serializable {
    private static final long serialVersionUID = 1L;

    private Integer id;
    private String type; // 枚举值：饮食/运动（数据库ENUM映射为String）
    private String name;
    private Integer days;
    private String description;
    private String url;
}