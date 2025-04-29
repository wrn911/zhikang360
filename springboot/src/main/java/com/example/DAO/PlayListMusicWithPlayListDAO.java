package com.example.DAO;

import com.example.entity.MusicDetail;
import com.example.entity.PlayListMusic;
import com.fasterxml.jackson.annotation.JsonCreator;
import lombok.Data;

import java.util.List;

@Data

public class PlayListMusicWithPlayListDAO {
    // 当前播放列表id
    Integer nowPlayListId;
    // 最近历史播放列表id
    Integer historyPlayListId;
    // 当前播放列表音乐集合
    List<MusicDetail> nowPlayListMusics;
    // 历史播放列表音乐集合
    List<MusicDetail> historyPlayListMusics;
}
