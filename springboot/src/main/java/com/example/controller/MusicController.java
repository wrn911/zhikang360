package com.example.controller;


import com.example.DAO.MusicDTO;
import com.example.common.Result;
import com.example.entity.Music;
import com.example.entity.PlayList;
import com.example.entity.PlayListMusic;
import com.example.service.MusicService;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;

@RestController
@RequestMapping("/music")
public class MusicController { // written by djy 2025-4-14 22:00

    /** 音乐播放器思路
     *  1、前端在created钩子中首先调用createPlayListByUserId()方法，确保有当前播放列表
     *  2、正确返回之后随即调用getPlayListMusicByUserId()方法，向前端传递当前列表和历史列表及其音乐的内容
     *  3、前端如果要新加音乐到播放列表调用addToPlaylist方法
     *  4、前端如果想本地导入音乐调用addPersonMusic方法
     *  5、前端调用getMusicList方法得到个人导入的所有音乐
     */
    @Resource
    private MusicService musicService;

    // 得到对应userId的全部音乐
    @GetMapping("/list")
    public Result getMusicList() {
        return Result.success(musicService.listMusics());
    }

    // 创建PlayList播放列表
    @PostMapping("/playlist")
    public Result createPlaylist() {
        return Result.success(musicService.createPlaylist());
    }

    // 新加音乐至播放列表
    @PostMapping("/playlist/add")
    public Result addToPlaylist(@RequestBody MusicDTO musicDTO) {
        musicService.changeIfNow(musicDTO);
        return Result.success(musicService.addToPlaylist(musicDTO));
    }

    // 个人从本地导入音乐
    @PostMapping("/person/add")
    public Result addPersonMusic(Music music) {
        String title = music.getTitle();
        String musicUrl = music.getMusicUrl();
        String s = musicUrl;
        Long userId = music.getUserId();
        return Result.success(musicService.addPersonMusic(title, musicUrl, userId, s));
    }

    // 向前端传送列表及其数据
    @GetMapping("/getListByUserId")
    public Result getPlayListMusicByUserId() {
        return Result.success(musicService.getPlayListMusicByUserId());
    }

    // 判断用户是否已有当前播放列表，若没有则创建
    @PostMapping("/createListByUserId")
    public Result createPlayListByUserId() {
        return Result.success(musicService.createPlayListMusicByUserId());
    }


}

