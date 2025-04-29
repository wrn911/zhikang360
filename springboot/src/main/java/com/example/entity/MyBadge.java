package com.example.entity;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class MyBadge {
    private Integer id;
    private Long userId;
    private Integer badgeId;
    private boolean ifNew;
    public MyBadge(Long userId, Integer badgeId, boolean ifNew) {
        this.userId = userId;
        this.badgeId = badgeId;
        this.ifNew = ifNew;
    }
}
