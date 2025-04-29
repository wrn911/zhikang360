package com.example.entity;

import lombok.Data;

import java.time.LocalDateTime;

@Data
public class IllnessInfo {
    private Integer id;
    private Long userId;
    private String allergyType;
    private String allergyDetails;
    private String chronicDiseases;
    private String healthIssues;
    private LocalDateTime createTime;
    private LocalDateTime updateTime;
}
