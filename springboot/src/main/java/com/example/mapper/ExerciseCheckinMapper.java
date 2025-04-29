package com.example.mapper;

import com.example.DAO.CheckinCountDTO;
import com.example.entity.ExerciseCheckin;
import org.apache.ibatis.annotations.Select;

import java.util.Date;
import java.util.List;
import java.util.Map;

/**
 * 操作 exercise 表相关数据接口
 */
public interface ExerciseCheckinMapper {

    /**
     * 根据用户Id查询历史运动
     */
    @Select("select * from exercise_checkin where user_id = #{userId}")
    List<ExerciseCheckin> selectHistory(Long userId);

    /**
     * 新增
     */
    int insertBatch(List<Map> list);

    /**
     * 根据时间查询
     */
    List<ExerciseCheckin> selectByTime(Date begin, Date end);

    /**
     * 查询所有（可带简单条件）
     */
    List<ExerciseCheckin> selectAll(Map map);

    /**
     * 根据ID查询
     */
    ExerciseCheckin selectById(Long id);

    /**
     * 删除
     */
    int deleteById(Integer id);

    /**
     * 修改
     */
    int updateById(ExerciseCheckin exerciseCheckin);

    CheckinCountDTO selectCheckinCounts(Long userId);
}

