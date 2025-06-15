package com.example.mapper;

import com.example.entity.UserRecommendInfo;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface UserRecommendInfoMapper {
    UserRecommendInfo selectByUserId(Long userId);
    int insert(UserRecommendInfo info);
    int update(UserRecommendInfo info);
}

