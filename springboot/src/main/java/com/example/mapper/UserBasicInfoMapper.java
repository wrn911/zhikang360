package com.example.mapper;

import com.example.entity.UserBasicInfo;
import com.example.entity.UserCheckInfo;

import java.util.List;

public interface UserBasicInfoMapper {
    int insert(UserBasicInfo userBasicInfo);
    int insertCheckInfo(UserCheckInfo userCheckInfo);
    int deleteById(Integer userId);
    int updateById(UserBasicInfo userBasicInfo);
    int updateCheckInfo(UserCheckInfo userCheckInfo);
    UserBasicInfo selectById(Integer userId);
    UserCheckInfo selectCheckInfoById(Long userId);
    List<UserBasicInfo> selectAll(UserBasicInfo condition);
    List<UserCheckInfo> selectCheckInfoAll(UserCheckInfo userCheckInfo);
}
