package com.example.entity.DTO;

import lombok.Data;

@Data
public class SyncResponse {
    private String message;
    private Integer userId;
    private String updateType;
}
