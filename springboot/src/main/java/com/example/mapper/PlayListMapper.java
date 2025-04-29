package com.example.mapper;

import com.example.entity.Music;
import com.example.entity.PlayList;
import com.example.entity.PlayListMusic;
import org.apache.ibatis.annotations.Mapper;
import java.util.List;

@Mapper
public interface PlayListMapper {
    // 播放列表操作
    int insertPlayList(PlayList playList);
    int insertPlayListMusic(PlayListMusic playListMusic);
    PlayList selectByUserId(Long userId);
    PlayList selectNowByUserId(Long userId);
}
