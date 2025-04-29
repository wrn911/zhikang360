package com.example.mapper;

import com.example.entity.BadgeStandard;
import com.example.entity.MyBadge;
import org.apache.ibatis.annotations.Param;

import java.util.ArrayList;
import java.util.List;

public interface BadgeStandardMapper {
    int insert(BadgeStandard badgeStandard);
    int deleteById(Integer id);
    int updateById(BadgeStandard badgeStandard);
    BadgeStandard selectById(Integer id);
    List<BadgeStandard> selectAll(BadgeStandard condition);
    int insertPersonBadge(MyBadge myBadge);
    int updatePersonBadge(@Param("userId") Long userId, @Param("badgeId") Integer badgeId);
    List <MyBadge> selectPersonBadgeAll(MyBadge myBadge);
    Integer selectIdByTypeAndDays(@Param("type") String type,
                                  @Param("days") Integer days);
    ArrayList<BadgeStandard> selectEarnedBadges(@Param("userId") Long userId);
    List<BadgeStandard> selectEarnedNewBadges(@Param("userId") Long userId);
    ArrayList<BadgeStandard> selectUnownedBadges(@Param("userId") Long userId);
}