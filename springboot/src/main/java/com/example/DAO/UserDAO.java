package com.example.DAO;
import java.time.LocalDateTime;

import java.io.Serializable;

/**
 * 用户表
 */
public class UserDAO implements Serializable {
    private static final long serialVersionUID = 1L;

    /** 账号 */
    private String username;
    /** 密码 */
    private String password;
    /** 电话 */
    private String phone;

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }
}

