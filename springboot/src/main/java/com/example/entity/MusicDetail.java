package com.example.entity;

import java.time.LocalDateTime;

import java.io.Serializable;

import com.example.entity.Account;
import lombok.Data;
/**
 * 音乐表
 */
@Data
public class MusicDetail implements Serializable {
    private static final long serialVersionUID = 1L;
    private Integer id;
    /** 音乐ID */
    private Integer musicId;
    /** 音乐标题 */
    private String title;
    /** 音乐类型 */
    private String type;
    /** 持续时长 */
    private Long duration;
    /** 音乐文件URL */
    private String musicUrl;
    /** 用户是否收藏 */
    private boolean ifFavorite;
    /** 播放列表id */
    private Integer playListId;
    /** 列表序号 */
    private Integer location;
    /** 是否为正在播放歌曲 */
    private boolean ifNow;

}
