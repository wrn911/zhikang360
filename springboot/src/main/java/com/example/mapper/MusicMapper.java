package com.example.mapper;

import com.example.entity.Music;
import com.example.entity.PlayList;
import com.example.entity.PlayListMusic;
import org.apache.ibatis.annotations.Mapper;
import java.util.List;

@Mapper
public interface MusicMapper {
    // 音乐操作
    List<Music> selectMusicList(Long userId);

    // 音乐添加
    int insert(Music music);
}
