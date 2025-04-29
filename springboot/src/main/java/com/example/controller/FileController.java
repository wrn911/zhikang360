package com.example.controller;

import cn.hutool.core.io.FileUtil;
import cn.hutool.core.thread.ThreadUtil;
import cn.hutool.core.util.StrUtil;
import com.example.common.Result;
import com.example.context.BaseContext;
import com.example.entity.Music;
import com.example.mapper.AdminMapper;
import com.example.mapper.MusicMapper;
import com.example.service.MusicService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.OutputStream;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Objects;

/**
 * 文件接口
 */
@RestController
@RequestMapping("/files")
public class FileController {

    // 文件上传存储路径
    private static final String filePath = System.getProperty("user.dir") + "/files/";
    @Resource
    private MusicService musicService;
    @Value("${server.port:9090}")
    private String port;

    @Value("${ip:localhost}")
    private String ip;

    /**
     * 文件上传
     */
    @PostMapping("/upload")
    public Result upload(MultipartFile file) {
        String flag;
        //if (file == null) {
            //System.err.println("文件未正确上传，file为null");
            //return Result.error("404","文件未正确上传");
        //}

        if (file.isEmpty()) {
            System.err.println("上传的文件为空");
            return Result.error("405","上传的文件为空");
        }
        synchronized (FileController.class) {
            flag = System.currentTimeMillis() + "";
            ThreadUtil.sleep(1L);
        }
        String fileName = file.getOriginalFilename();
        try {
            if (!FileUtil.isDirectory(filePath)) {
                FileUtil.mkdir(filePath);
            }
            // 文件存储形式：时间戳-文件名
            FileUtil.writeBytes(file.getBytes(), filePath + flag + "-" + fileName);  // ***/manager/files/1697438073596-avatar.png
            System.out.println(fileName + "--上传成功");

        } catch (Exception e) {
            System.err.println(fileName + "--文件上传失败");
        }
        String http = "http://" + ip + ":" + port + "/files/";
        return Result.success(http + flag + "-" + fileName);  //  http://localhost:9090/files/1697438073596-avatar.png
    }

    @PostMapping("/music/upload")
    public Result uploadMusic(
            @RequestParam("music") MultipartFile file,
            @RequestParam("userId") Long userId) {
        // 验证用户ID有效性
        if (userId == null || userId <= 0) {
            return Result.error("401", "用户身份验证失败");
        }
        // 参数校验改进
        if (file.isEmpty()) {
            System.err.println("上传的音乐文件为空");
            return Result.error("405","上传的文件为空");
        }

        // 增强文件类型校验（同时校验MIME类型和扩展名）
        String contentType = file.getContentType();
        String originalFilename = file.getOriginalFilename();
        if (!Objects.equals(contentType, "audio/mpeg") ||
                !originalFilename.toLowerCase().endsWith(".mp3")) {
            System.err.println("非法文件类型：" + contentType + " | " + originalFilename);
            return Result.error("408", "仅支持MP3格式");
        }
        int lastDotIndex = originalFilename.lastIndexOf('.');
        String fileNameWithoutExtension = (lastDotIndex > 0)
                ? originalFilename.substring(0, lastDotIndex)
                : originalFilename;
        // 修正文件大小错误描述
        long MAX_SIZE = 30 * 1024 * 1024;
        if (file.getSize() > MAX_SIZE) {
            System.err.println("文件过大：" + file.getSize());
            return Result.error("413", "文件大小超过30MB限制");
        }

        String flag;
        try {
            // 同步块生成唯一标识（与原方法保持一致）
            synchronized (FileController.class) {
                flag = System.currentTimeMillis() + "";
                ThreadUtil.sleep(1L);
            }

            // 构建存储路径
            String userDir = "user_" + userId;
            String storagePath = filePath + "/music/" + userDir + "/";

            if (!FileUtil.isDirectory(storagePath)) {
                FileUtil.mkdir(storagePath);
            }

            String encodedFileName = URLEncoder.encode(originalFilename, StandardCharsets.UTF_8.name());
            String saveName = flag + "-" + encodedFileName;

            String phyPath = storagePath + saveName;

            // 文件存储（保持与原方法相同写法）
            FileUtil.writeBytes(file.getBytes(), storagePath + saveName);
            System.out.println(originalFilename + "--音乐上传成功");

            // 构建访问URL
            String accessUrl = "http://" + ip + ":" + port + "/files/music/"
                    + userDir + "/" + saveName;

            Music music = new Music();
            music.setMusicUrl(accessUrl);
            music.setTitle(fileNameWithoutExtension);
            musicService.addPersonMusic(fileNameWithoutExtension, accessUrl, userId, phyPath);
            return Result.success(music);

        } catch (IOException e) {
            System.err.println("文件存储失败: " + e.getMessage());
            return Result.error("500", "文件存储失败");
        } catch (Exception e) {
            System.err.println("未知错误: " + e.getMessage());
            return Result.error("500", "服务器内部错误");
        }
    }



    /**
     * 获取文件
     *
     * @param flag
     * @param response
     */
    @GetMapping("/{flag}")   //  1697438073596-avatar.png
    public void avatarPath(@PathVariable String flag, HttpServletResponse response) {
        OutputStream os;
        try {
            if (StrUtil.isNotEmpty(flag)) {
                response.addHeader("Content-Disposition", "attachment;filename=" + URLEncoder.encode(flag, "UTF-8"));
                response.setContentType("application/octet-stream");
                byte[] bytes = FileUtil.readBytes(filePath + flag);
                os = response.getOutputStream();
                os.write(bytes);
                os.flush();
                os.close();
            }
        } catch (Exception e) {
            System.out.println("文件下载失败");
        }
    }

    /**
     * 删除文件
     *
     * @param flag
     */
    @DeleteMapping("/{flag}")
    public void delFile(@PathVariable String flag) {
        FileUtil.del(filePath + flag);
        System.out.println("删除文件" + flag + "成功");
    }


}
