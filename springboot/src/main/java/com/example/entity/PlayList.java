package com.example.entity;

import java.time.LocalDateTime;

import java.io.Serializable;

import com.example.entity.Account;
import lombok.Data;
/**
 * 用户音乐播放列表
 */
@Data
public class PlayList implements Serializable {
    private static final long serialVersionUID = 1L;
    /** 播放列表id */
    private Integer playListId;
    /** 用户ID */
    private Long userId;
    /** 是否为正在播放队列 */
    private boolean ifNow;
}

