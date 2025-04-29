package com.example.entity;

import java.time.LocalDateTime;

import java.io.Serializable;

import com.example.entity.Account;
import lombok.Data;
/**
 * 音乐表
 */
@Data
public class Music implements Serializable {
    private static final long serialVersionUID = 1L;

    /** 音乐ID */
    private Integer musicId;
    /** 用户ID */
    private Long userId;
    /** 音乐标题 */
    private String title;
    /** 音乐类型 */
    private String type;
    /** 持续时长 */
    private Long duration;
    /** 音乐文件URL */
    private String musicUrl;
    /** 播放次数 */
    private Integer playCount;
    /** 用户是否收藏 */
    private boolean ifFavorite;
    /** 创建时间 */
    private LocalDateTime createTime;

}
