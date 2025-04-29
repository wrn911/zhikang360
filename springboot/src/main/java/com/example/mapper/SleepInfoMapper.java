package com.example.mapper;

import com.example.entity.SleepInfo;
import java.util.List;

public interface SleepInfoMapper {

    // 根据用户ID查询睡眠信息
    SleepInfo selectByUserId(Long userId);

    // 新增睡眠信息
    int insert(SleepInfo sleepInfo);

    // 根据ID更新睡眠信息
    int updateById(SleepInfo sleepInfo);

    // 注：XML中未定义deleteById，可根据需要补充
}
