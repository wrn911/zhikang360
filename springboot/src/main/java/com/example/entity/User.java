package com.example.entity;
import java.time.LocalDateTime;

import java.io.Serializable;
import lombok.Data;
/**
 * 用户表
 */
@Data
public class User extends Account implements Serializable {
    private static final long serialVersionUID = 1L;

    /** ID */
    private Integer id;
    /** 账号 */
    private String username;
    /** 密码 */
    private String password;
    /** 头像 */
    private String avatar;
    /** 电话 */
    private String phone;

    private boolean if_new;

    private LocalDateTime register_time;

    private LocalDateTime last_time;

    private String role;

}
