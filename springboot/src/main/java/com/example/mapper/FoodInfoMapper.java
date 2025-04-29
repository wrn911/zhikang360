package com.example.mapper;

import com.example.entity.FoodInfo;
import java.util.List;

public interface FoodInfoMapper {

    // 根据用户ID查询饮食信息
    FoodInfo selectByUserId(Long userId);

    // 新增饮食信息
    int insert(FoodInfo foodInfo);

    // 根据ID更新饮食信息
    int updateById(FoodInfo foodInfo);

    // 根据ID删除记录（XML中存在此操作）
    int deleteById(Integer id);
}
