package com.example.entity;

import java.time.LocalDateTime;

import java.io.Serializable;

import com.example.entity.Account;
import lombok.Data;
/**
 * 音乐播放列曲目表
 */
@Data
public class PlayListMusic implements Serializable {
    private static final long serialVersionUID = 1L;
    /** 播放列表id */
    private Integer id;
    /** 播放列表id */
    private Integer playListId;
    /** 音乐ID */
    private Integer musicId;
    /** 用户ID */
    private Long userId;
    /** 持续时长 */
    private Integer location;
    /** 音乐文件URL */
    private String musicUrl;
    /** 是否为正在播放歌曲 */
    private boolean ifNow;

}
