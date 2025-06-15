package com.example.service;

import com.example.utils.TokenUtils;
import com.example.common.Constants;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

import javax.servlet.http.HttpServletRequest;

@Service
public class PythonHealthSyncService {

    @Autowired
    private RestTemplate restTemplate;

    @Value("${python.backend.url:http://localhost:8000}")
    private String pythonBackendUrl;

    private static final Logger logger = LoggerFactory.getLogger(PythonHealthSyncService.class);

    /**
     * 获取当前请求的token
     */
    private String getCurrentToken() {
        try {
            ServletRequestAttributes attributes = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
            if (attributes != null) {
                HttpServletRequest request = attributes.getRequest();
                String token = request.getHeader(Constants.TOKEN);
                if (token == null || token.isEmpty()) {
                    token = request.getParameter(Constants.TOKEN);
                }
                return token;
            }
        } catch (Exception e) {
            logger.warn("无法获取当前请求的token: {}", e.getMessage());
        }
        return null;
    }

    /**
     * 创建带token的HTTP请求头
     */
    private HttpHeaders createHeadersWithToken() {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        String token = getCurrentToken();
        if (token != null && !token.isEmpty()) {
            headers.set(Constants.TOKEN, token);
            logger.debug("添加token到请求头: {}", token);
        } else {
            logger.warn("未找到有效的token，可能会导致Python接口调用失败");
        }

        return headers;
    }

    /**
     * 同步用户健康数据到Python后端
     */
    public SyncResponse syncUserHealthData(Integer userId, Boolean forceUpdate) {
        try {
            String url = pythonBackendUrl + "/health-data/sync/" + userId;

            // 构建请求体
            SyncRequest request = new SyncRequest(forceUpdate);

            // 创建带token的请求头
            HttpHeaders headers = createHeadersWithToken();
            HttpEntity<SyncRequest> entity = new HttpEntity<>(request, headers);

            // 发送POST请求
            ResponseEntity<SyncResponse> response = restTemplate.exchange(
                    url,
                    HttpMethod.POST,
                    entity,
                    SyncResponse.class
            );

            if (response.getStatusCode() == HttpStatus.OK) {
                logger.info("用户{}健康数据同步成功: {}", userId, response.getBody().getMessage());
                return response.getBody();
            } else {
                logger.error("用户{}健康数据同步失败, 状态码: {}", userId, response.getStatusCode());
                throw new RuntimeException("健康数据同步失败");
            }

        } catch (Exception e) {
            logger.error("调用Python健康数据同步接口失败, 用户ID: {}, 错误: {}", userId, e.getMessage(), e);
            throw new RuntimeException("健康数据同步服务异常: " + e.getMessage());
        }
    }

    /**
     * 异步同步健康数据（用于用户操作后的自动同步）
     * 注意：异步调用时无法获取到请求上下文中的token
     */
    @Async
    public void asyncSyncUserHealthData(Integer userId) {
        try {
            // 对于异步调用，我们需要特殊处理token
            syncUserHealthDataWithGeneratedToken(userId, false);
        } catch (Exception e) {
            logger.error("异步同步用户{}健康数据失败: {}", userId, e.getMessage());
        }
    }

    /**
     * 使用生成的token进行同步（用于异步调用）
     */
    private SyncResponse syncUserHealthDataWithGeneratedToken(Integer userId, Boolean forceUpdate) {
        try {
            String url = pythonBackendUrl + "/health-data/sync/" + userId;

            // 构建请求体
            SyncRequest request = new SyncRequest(forceUpdate);

            // 为异步调用生成token
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            // 生成系统级token（需要先获取用户信息）
            String systemToken = generateSystemTokenForUser(userId);
            if (systemToken != null) {
                headers.set(Constants.TOKEN, systemToken);
            }

            HttpEntity<SyncRequest> entity = new HttpEntity<>(request, headers);

            // 发送POST请求
            ResponseEntity<SyncResponse> response = restTemplate.exchange(
                    url,
                    HttpMethod.POST,
                    entity,
                    SyncResponse.class
            );

            if (response.getStatusCode() == HttpStatus.OK) {
                logger.info("用户{}健康数据异步同步成功: {}", userId, response.getBody().getMessage());
                return response.getBody();
            } else {
                logger.error("用户{}健康数据异步同步失败, 状态码: {}", userId, response.getStatusCode());
                throw new RuntimeException("健康数据异步同步失败");
            }

        } catch (Exception e) {
            logger.error("异步调用Python健康数据同步接口失败, 用户ID: {}, 错误: {}", userId, e.getMessage(), e);
            throw new RuntimeException("健康数据异步同步服务异常: " + e.getMessage());
        }
    }

    /**
     * 为指定用户生成系统级token（用于异步调用）
     */
    private String generateSystemTokenForUser(Integer userId) {
        try {
            // 这里需要注入UserService来获取用户信息
            // 为了简化，我们使用一个工具方法
            return TokenUtils.generateTokenForUser(userId);
        } catch (Exception e) {
            logger.error("为用户{}生成系统token失败: {}", userId, e.getMessage());
            return null;
        }
    }

    // 内部类：请求和响应DTO
    public static class SyncRequest {
        private Boolean forceUpdate = false;

        public SyncRequest() {}

        public SyncRequest(Boolean forceUpdate) {
            this.forceUpdate = forceUpdate;
        }

        public Boolean getForceUpdate() {
            return forceUpdate;
        }

        public void setForceUpdate(Boolean forceUpdate) {
            this.forceUpdate = forceUpdate;
        }
    }

    public static class SyncResponse {
        private String message;
        private Integer userId;
        private String updateType;

        // getter和setter
        public String getMessage() {
            return message;
        }

        public void setMessage(String message) {
            this.message = message;
        }

        public Integer getUserId() {
            return userId;
        }

        public void setUserId(Integer userId) {
            this.userId = userId;
        }

        public String getUpdateType() {
            return updateType;
        }

        public void setUpdateType(String updateType) {
            this.updateType = updateType;
        }
    }
}