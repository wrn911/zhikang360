package com.example.mapper;

import com.example.entity.Music;
import com.example.entity.MusicDetail;
import com.example.entity.PlayList;
import com.example.entity.PlayListMusic;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface PlayListMusicMapper {
    // 播放列表操作
    int insertPlayListMusic(PlayListMusic playListMusic);
    List <PlayListMusic> selectNowPlayListMusic(@Param("userId") Long userId);

    int updatePlayListMusics(PlayListMusic playListMusic);
    PlayListMusic selectNowLocation(Long userId);

    List <MusicDetail> selectMusicDetailByPlayListId(Long userId, Integer playListId);
}
