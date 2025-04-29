package com.example.entity;

import lombok.Data;

import java.io.Serializable;
import java.util.List;

/**
 * 攻略信息表
*/
@Data
public class Introduction implements Serializable {
    private static final long serialVersionUID = 1L;

    private Integer id;
    private String name;
    private String img;
    private String content;
    private Integer comment;
    private Integer collect;
    private Integer views;
    private String time;
    private Integer userId;

    private String description;

    private String userName;
    private String userAvatar;

    private List<Comment> comments;//评论
    private Integer collected;//已点赞
}