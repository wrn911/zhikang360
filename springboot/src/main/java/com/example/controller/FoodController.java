package com.example.controller;

import com.example.common.Result;
import com.example.entity.Food;
import com.example.service.FoodService;
import com.github.pagehelper.PageInfo;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.List;

/**
 * 食物信息前端操作接口
 */
@RestController
@RequestMapping("/food")
public class FoodController {

    @Resource
    private FoodService foodService;

    /**
     * 新增
     */
    @PostMapping("/add")
    public Result add(@RequestBody Food food) {
        foodService.add(food);
        return Result.success();
    }

    /**
     * 删除
     */
    @DeleteMapping("/delete/{id}")
    public Result deleteById(@PathVariable Integer id) {
        foodService.deleteById(id);
        return Result.success();
    }

    /**
     * 批量删除
     */
    @DeleteMapping("/delete/batch")
    public Result deleteBatch(@RequestBody List<Integer> ids) {
        foodService.deleteBatch(ids);
        return Result.success();
    }

    /**
     * 修改
     */
    @PutMapping("/update")
    public Result updateById(@RequestBody Food food) {
        foodService.updateById(food);
        return Result.success();
    }

    /**
     * 根据ID查询
     */
    @GetMapping("/selectById/{id}")
    public Result selectById(@PathVariable Integer id) {
        Food food = foodService.selectById(id);
        return Result.success(food);
    }

    /**
     * 查询所有
     */
    @GetMapping("/selectAll")
    public Result selectAll(Food food) {
        List<Food> list = foodService.selectAll(food);
        return Result.success(list);
    }

    /**
     * 分页查询
     */
    @GetMapping("/selectPage")
    public Result selectPage(Food food,
                             @RequestParam(defaultValue = "1") Integer pageNum,
                             @RequestParam(defaultValue = "10") Integer pageSize) {
        PageInfo<Food> page = foodService.selectPage(food, pageNum, pageSize);
        return Result.success(page);
    }
}

