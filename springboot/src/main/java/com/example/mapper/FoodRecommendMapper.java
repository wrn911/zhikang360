package com.example.mapper;

import com.example.entity.FoodRecommend;
import com.example.entity.FoodRecommendList;
import com.example.entity.UserFoodRecommendList;
import org.apache.ibatis.annotations.*;

import java.time.LocalDate;
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
    List<UserFoodRecommendList> selectByAimAndGroceryAndTime(@Param("userId") Long userId,
                                                             @Param("aim") String aim,
                                                             @Param("grocery") String grocery,
                                                             @Param("time") String time);
    void insertUserFoodRecommendFromTemplate(@Param("userId") Long userId);

    List<UserFoodRecommendList> selectTodayRecommendedFoods(
            @Param("userId") Long userId,
            @Param("targetDate") LocalDate targetDate
    );

    UserFoodRecommendList selectUserFoodRecommendListById(@Param("id") Integer id);

    void updateWeight(@Param("id") Integer id,
                      @Param("weight") Double weight);

}
