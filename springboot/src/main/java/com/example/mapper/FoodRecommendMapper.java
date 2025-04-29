package com.example.mapper;

import com.example.entity.FoodRecommend;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface FoodRecommendMapper {

    // 移除了SQL注解，全部通过XML实现
    int insert(FoodRecommend record);

    int deleteById(@Param("recommendId") Integer recommendId);

    int updatePortion(@Param("recommendId") Integer recommendId,
                      @Param("gramAte") Integer gramAte,
                      @Param("caloriesAte") Double caloriesAte);

    FoodRecommend selectById(@Param("recommendId") Integer recommendId);

    List<FoodRecommend> selectByUserId(@Param("userId") Long userId);

    List<FoodRecommend> selectByUserIdAndDate(@Param("userId") Long userId,
                                              @Param("date") String date);
}
