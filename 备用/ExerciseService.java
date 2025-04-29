package com.example.service;

import com.example.entity.Exercise;
import com.example.mapper.ExerciseMapper;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

/**
 * 运动信息业务处理
 */
@Service
public class ExerciseService {

    @Resource
    private ExerciseMapper exerciseMapper;

    /**
     * 新增
     */
    public void add(Exercise exercise) {
        // 如果需要记录创建时间或创建人，可以在此处补充
        exerciseMapper.insert(exercise);
    }

    /**
     * 删除
     */
    public void deleteById(Integer id) {
        exerciseMapper.deleteById(id);
    }

    /**
     * 批量删除
     */
    public void deleteBatch(List<Integer> ids) {
        for (Integer id : ids) {
            exerciseMapper.deleteById(id);
        }
    }

    /**
     * 修改
     */
    public void updateById(Exercise exercise) {
        exerciseMapper.updateById(exercise);
    }

    /**
     * 根据ID查询
     */
    public Exercise selectById(Integer id) {
        return exerciseMapper.selectById(id);
    }

    /**
     * 查询所有
     */
    public List<Exercise> selectAll(Exercise exercise) {
        return exerciseMapper.selectAll(exercise);
    }

    /**
     * 分页查询
     */
    public PageInfo<Exercise> selectPage(Exercise exercise, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum, pageSize);
        List<Exercise> list = exerciseMapper.selectAll(exercise);
        return PageInfo.of(list);
    }
}
