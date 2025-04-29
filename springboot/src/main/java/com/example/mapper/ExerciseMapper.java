package com.example.mapper;

import com.example.entity.Exercise;
import com.example.entity.ExerciseCheckin;
import org.apache.ibatis.annotations.Select;

import java.util.List;

/**
 * 操作 exercise 表相关数据接口
 */
public interface ExerciseMapper {

    /**
     * 根据用户Id查询历史运动
     */
    @Select("select * from exercise_checkin where user_id = #{userId}")
    List<ExerciseCheckin> selectHistory(Long userId);


    /**
     * 新增
     */
    int insert(Exercise exercise);

    /**
     * 删除
     */
    int deleteById(Integer id);

    /**
     * 修改
     */
    int updateById(Exercise exercise);

    /**
     * 根据ID查询
     */
    Exercise selectById(Integer id);

    /**
     * 查询所有（可带简单条件）
     */
    List<Exercise> selectAll(Exercise exercise);
}

