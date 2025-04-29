package com.example.controller;

import com.example.common.Result;
import com.example.entity.BadgeStandard;
import com.example.service.BadgeStandardService;
import com.github.pagehelper.PageInfo;
import org.springframework.web.bind.annotation.*;
import javax.annotation.Resource;

@RestController
@RequestMapping("/badgeStandard")
public class BadgeStandardController {

    @Resource
    private BadgeStandardService badgeStandardService;

    @PostMapping("/add")
    public Result add(@RequestBody BadgeStandard badgeStandard) {
        badgeStandardService.add(badgeStandard);
        return Result.success();
    }

    @DeleteMapping("/delete/{id}")
    public Result deleteById(@PathVariable Integer id) {
        badgeStandardService.deleteById(id);
        return Result.success();
    }

    @PutMapping("/update")
    public Result updateById(@RequestBody BadgeStandard badgeStandard) {
        badgeStandardService.updateById(badgeStandard);
        return Result.success();
    }

    @GetMapping("/selectById/{id}")
    public Result selectById(@PathVariable Integer id) {
        return Result.success(badgeStandardService.selectById(id));
    }

    @GetMapping("/selectPage")
    public Result selectPage(BadgeStandard condition,
                             @RequestParam(defaultValue = "1") Integer pageNum,
                             @RequestParam(defaultValue = "10") Integer pageSize) {
        PageInfo<BadgeStandard> page = badgeStandardService.selectPage(condition, pageNum, pageSize);
        return Result.success(page);
    }

    @GetMapping("/selectByUserId")
    public Result selectByUserId() {
        return Result.success(badgeStandardService.selectByUserId());
    }

    @GetMapping("/selectEarnedNewBadges")
    public Result selectEarnedNewBadges() {
        return Result.success(badgeStandardService.selectEarnedNewBadges());
    }
}