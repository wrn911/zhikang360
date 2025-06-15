package com.example.utils;

import cn.hutool.core.date.DateUtil;
import cn.hutool.core.util.ObjectUtil;
import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.example.common.Constants;
import com.example.common.enums.RoleEnum;
import com.example.entity.Account;
import com.example.service.AdminService;
import com.example.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

import javax.annotation.PostConstruct;
import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import java.util.Date;

/**
 * Token工具类
 */
@Component
public class TokenUtils {

    private static final Logger log = LoggerFactory.getLogger(TokenUtils.class);

    private static AdminService staticAdminService;
    private static UserService staticUserService;

    @Resource
    UserService userService;

    @Resource
    AdminService adminService;

    @PostConstruct
    public void setServices() {
        staticAdminService = adminService;
        staticUserService = userService;  // 添加这行
    }

    /**
     * 生成token
     */
    public static String createToken(String data, String sign) {
        return JWT.create().withAudience(data) // 将 userId-role 保存到 token 里面,作为载荷
                .withExpiresAt(DateUtil.offsetHour(new Date(), 2)) // 2小时后token过期
                .sign(Algorithm.HMAC256(sign)); // 以 password 作为 token 的密钥
    }

    /**
     * 获取当前登录的用户信息
     */
    public static Account getCurrentUser() {
        try {
            HttpServletRequest request = ((ServletRequestAttributes) RequestContextHolder.getRequestAttributes()).getRequest();
            String token = request.getHeader(Constants.TOKEN);
            if (ObjectUtil.isNotEmpty(token)) {
                String userRole = JWT.decode(token).getAudience().get(0);
                String userId = userRole.split("-")[0];  // 获取用户id
                String role = userRole.split("-")[1];    // 获取角色
                if (RoleEnum.ADMIN.name().equals(role)) {
                    return staticAdminService.selectById(Integer.valueOf(userId));
                }
            }
        } catch (Exception e) {
            log.error("获取当前用户信息出错", e);
        }
        return new Account();  // 返回空的账号对象
    }

    /**
     * 为指定用户生成token（用于系统内部调用）
     */
    public static String generateTokenForUser(Integer userId) {
        try {
            // 假设是USER角色，如果需要支持ADMIN，可以添加参数
            String userRole = userId + "-" + RoleEnum.USER.name();

            // 这里需要获取用户密码作为签名
            // 你需要注入UserService
            Account user = staticUserService.selectById(userId);
            if (user != null && user.getPassword() != null) {
                return createToken(userRole, user.getPassword());
            } else {
                log.error("无法为用户{}生成token：用户不存在或密码为空", userId);
                return null;
            }
        } catch (Exception e) {
            log.error("为用户{}生成token时出错", userId, e);
            return null;
        }
    }
}

