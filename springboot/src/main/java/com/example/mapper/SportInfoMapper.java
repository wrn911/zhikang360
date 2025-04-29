package com.example.mapper;

import com.example.entity.SportInfo;
import java.util.List;

public interface SportInfoMapper {

    // 根据用户ID查询运动信息
    SportInfo selectByUserId(Long userId);

    // 新增运动信息
    int insert(SportInfo sportInfo);

    // 根据ID更新运动信息
    int updateById(SportInfo sportInfo);

    // 注：XML中未定义deleteById，可根据需要补充
}