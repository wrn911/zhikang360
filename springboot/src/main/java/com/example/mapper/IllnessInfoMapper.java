package com.example.mapper;

import com.example.entity.IllnessInfo;
import java.util.List;

public interface IllnessInfoMapper {

    // 根据用户ID查询健康信息
    IllnessInfo selectByUserId(Long userId);

    // 新增健康信息
    int insert(IllnessInfo illnessInfo);

    // 根据ID更新健康信息
    int updateById(IllnessInfo illnessInfo);

    // 注：XML中未定义deleteById，可根据需要补充
}
