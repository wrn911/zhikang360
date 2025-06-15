package com.example.service;

import com.example.DAO.MusicDTO;
import com.example.DAO.PlayListMusicWithPlayListDAO;
import com.example.common.Result;
import com.example.entity.*;
import com.example.mapper.MusicMapper;
import com.example.context.BaseContext;
import com.example.common.enums.MusicTypeEnum;

import java.io.File;
import java.net.MalformedURLException;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.net.URL;
import javax.annotation.Resource;
import javax.sound.sampled.*;
import java.util.Map;

import com.example.mapper.PlayListMapper;
import com.example.mapper.PlayListMusicMapper;
import org.springframework.stereotype.Service;
import com.mpatric.mp3agic.Mp3File;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import com.example.entity.Music;


@Service
public class MusicService {
    @Resource
    private MusicMapper musicMapper;
    @Resource
    private PlayListMapper playListMapper;
    @Resource
    private PlayListMusicMapper playListMusicMapper;

    // 从音乐表中获得所有音乐
    public List<Music> listMusics() {
        Long userId = BaseContext.getCurrentId();
        return musicMapper.selectMusicList(userId);
    }

    // 创建新的播放列表
    public int createPlaylist() {
        PlayList playList = new PlayList();
        Long userId = BaseContext.getCurrentId();
        playList.setIfNow(true);
        playList.setUserId(userId);
        return playListMapper.insertPlayList(playList);
    }

    // 向前端传送列表及其数据
    public PlayListMusicWithPlayListDAO getPlayListMusicByUserId(){
        PlayListMusicWithPlayListDAO playListMusicWithPlayListDAO = new PlayListMusicWithPlayListDAO();
        Long userId = BaseContext.getCurrentId();
        PlayList historyPlayList = playListMapper.selectByUserId(userId);
        Integer historyPlayListId;
        List<MusicDetail> historyPlayListMusics;
        if(historyPlayList == null){
            historyPlayListId = null;
            historyPlayListMusics = null;
        }else{
            historyPlayListId = historyPlayList.getPlayListId();
            historyPlayListMusics = playListMusicMapper.selectMusicDetailByPlayListId(userId, historyPlayListId);
        }
        PlayList nowPlayList = playListMapper.selectNowByUserId(userId);
        Integer nowPlayListId = nowPlayList.getPlayListId();
        List<MusicDetail> nowPlayListMusics = playListMusicMapper.selectMusicDetailByPlayListId(userId, nowPlayListId);
        playListMusicWithPlayListDAO.setHistoryPlayListId(historyPlayListId);
        playListMusicWithPlayListDAO.setNowPlayListId(nowPlayListId);
        playListMusicWithPlayListDAO.setHistoryPlayListMusics(historyPlayListMusics);
        playListMusicWithPlayListDAO.setNowPlayListMusics(nowPlayListMusics);
        return  playListMusicWithPlayListDAO;
    }

    // 新加音乐至播放列表
    public int addToPlaylist(MusicDTO music) {
        Long userId = BaseContext.getCurrentId();
        PlayList nowPlayList = playListMapper.selectNowByUserId(userId);
        Integer nowPlayListId = nowPlayList.getPlayListId();
        List<PlayListMusic> playListMusics = playListMusicMapper.selectNowPlayListMusic(userId);
        PlayListMusic playListMusic = playListMusicMapper.selectNowLocation(userId);
        if(playListMusic == null){
            playListMusic = new PlayListMusic();
            playListMusic.setPlayListId(nowPlayListId);
            playListMusic.setLocation(0);
            playListMusic.setId(null);
            playListMusic.setMusicUrl(music.getMusicUrl());
            playListMusic.setMusicId(music.getMusicId());
            playListMusic.setIfNow(true);
        }else{
            Integer nowLocation = playListMusic.getLocation();
            for(PlayListMusic plm : playListMusics){
                if(plm.getLocation() > nowLocation){
                    plm.setLocation(plm.getLocation() + 1);
                    playListMusicMapper.updatePlayListMusics(plm);
                }
            }
            playListMusic.setLocation(nowLocation + 1);
            playListMusic.setId(null);
            playListMusic.setMusicUrl(music.getMusicUrl());
            playListMusic.setMusicId(music.getMusicId());
            playListMusic.setIfNow(false);
        }
        playListMusic.setUserId(userId);
        return playListMusicMapper.insertPlayListMusic(playListMusic);
    }

    // 个人从本地导入音乐
    public int addPersonMusic(String title, String musicUrl, Long userId, String storagePath){
        long duration = 0;

        // 优先使用 ffprobe 获取时长
        try {
            String ffprobePath = "D:\\program files\\ffmpeg\\ffmpeg-7.1.1-essentials_build\\bin\\ffprobe.exe"; // <-- 注意换成你自己的路径
            ProcessBuilder pb = new ProcessBuilder(
                    ffprobePath, "-v", "error",
                    "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1",
                    storagePath
            );
            pb.redirectErrorStream(true);
            Process process = pb.start();
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                String line = reader.readLine();
                if (line != null) {
                    double seconds = Double.parseDouble(line.trim());
                    duration = (long) seconds;
                    System.out.println("使用ffprobe获取时长成功：" + duration + " 秒");
                }
            }
            process.waitFor();
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("ffprobe解析失败，尝试其他方法获取时长...");
        }

        // 如果ffprobe失败，兜底用mp3agic解析
        if (duration == 0) {
            try {
                Mp3File mp3File = new Mp3File(storagePath);
                if (mp3File.hasId3v1Tag() || mp3File.hasId3v2Tag()) {
                    duration = mp3File.getLengthInSeconds();
                    System.out.println("使用mp3agic获取时长成功：" + duration + " 秒");
                }
            } catch (Exception e) {
                e.printStackTrace();
                System.out.println("mp3agic解析失败，时长保持为0秒");
            }
        }

        Music music = new Music();
        music.setUserId(userId);
        music.setTitle(title);
        music.setDuration(duration);
        music.setMusicUrl(musicUrl);
        music.setType(MusicTypeEnum.个人导入.name());
        music.setPlayCount(0);
        music.setIfFavorite(true);
        music.setCreateTime(LocalDateTime.now());
        return musicMapper.insert(music);
    }


    public int addPersonMusic1(String title, String musicUrl, Long userId, String storagePath){
        long duration = 0 ;
        /*try{
            File audioFile = new File(storagePath);
            AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(audioFile);
            duration = audioInputStream.getFrameLength() / (int) audioInputStream.getFormat().getFrameRate();
        }catch(UnsupportedAudioFileException e){
            e.printStackTrace();
        }catch(IOException e){
            e.printStackTrace();
        }*/

        /*try {
            // 1. 获取文件格式
            AudioFileFormat format = AudioSystem.getAudioFileFormat(mp3File);
            System.out.println("文件类型: " + format.getType());

            // 2. 获取音频流并计算时长
            try (AudioInputStream stream = AudioSystem.getAudioInputStream(mp3File)) {
                AudioFormat audioFormat = stream.getFormat();
                long frames = stream.getFrameLength();
                duration = (long) (frames / audioFormat.getFrameRate());
                System.out.printf("时长: %d 秒%n", duration);
            }
        } catch (UnsupportedAudioFileException e) {
            System.err.println("不支持的音频格式: " + e.getMessage());
        } catch (IOException e) {
            System.err.println("文件读取错误: " + e.getMessage());
        }*/
        try {
            Mp3File mp3File = new Mp3File(storagePath);
            if (mp3File.hasId3v1Tag() || mp3File.hasId3v2Tag()) {
                duration = mp3File.getLengthInSeconds(); // 获取时长（秒）
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        Music music = new Music();
        music.setUserId(userId);
        music.setTitle(title);
        music.setDuration(duration);
        music.setMusicUrl(musicUrl);
        music.setType(MusicTypeEnum.个人导入.name());
        music.setPlayCount(0);
        music.setIfFavorite(true);
        music.setCreateTime(LocalDateTime.now());
        return musicMapper.insert(music);
    }

    // 判断用户是否已有当前播放列表，若没有则创建
    public int createPlayListMusicByUserId() {
        Long userId = BaseContext.getCurrentId();
        PlayList playList = playListMapper.selectNowByUserId(userId);
        if(playList == null){
            playList = new PlayList();
            playList.setUserId(userId);
            playList.setIfNow(true);
            return playListMapper.insertPlayList(playList);
        }else{
            return 1;
        }
    }

    public void changeIfNow(MusicDTO musicDTO) {
        Long userId = BaseContext.getCurrentId();
        PlayList nowPlayList = playListMapper.selectNowByUserId(userId);
        Integer nowPlayListId = nowPlayList.getPlayListId();
        List<PlayListMusic> playListMusics = playListMusicMapper.selectNowPlayListMusic(userId);
        PlayListMusic playListMusic = playListMusicMapper.selectNowLocation(userId);
        playListMusic.setIfNow(false);
        playListMusicMapper.updatePlayListMusics(playListMusic);
        int location = musicDTO.getCurrentSong().getLocation();
        for(PlayListMusic plm : playListMusics){
            if(plm.getLocation() == location){
                plm.setIfNow(true);
                playListMusicMapper.updatePlayListMusics(plm);
            }
        }
    }
}
