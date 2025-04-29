package com.example.service;

import com.example.entity.Food;
import com.example.mapper.FoodMapper;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

/**
 * 食物信息业务处理
 */
@Service
public class FoodService {

    @Resource
    private FoodMapper foodMapper;

    /**
     * 新增
     */
    public void add(Food food) {
        // 如果需要记录创建时间或创建人，可以在这里补充
        foodMapper.insert(food);
    }

    /**
     * 删除
     */
    public void deleteById(Integer id) {
        foodMapper.deleteById(id);
    }

    /**
     * 批量删除
     */
    public void deleteBatch(List<Integer> ids) {
        for (Integer id : ids) {
            foodMapper.deleteById(id);
        }
    }

    /**
     * 修改
     */
    public void updateById(Food food) {
        foodMapper.updateById(food);
    }

    /**
     * 根据ID查询
     */
    public Food selectById(Integer id) {
        return foodMapper.selectById(id);
    }

    /**
     * 查询所有
     */
    public List<Food> selectAll(Food food) {
        return foodMapper.selectAll(food);
    }

    /**
     * 分页查询
     */
    public PageInfo<Food> selectPage(Food food, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum, pageSize);
        List<Food> list = foodMapper.selectAll(food);
        return PageInfo.of(list);
    }
}

