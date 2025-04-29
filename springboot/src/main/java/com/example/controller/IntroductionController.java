package com.example.controller;

import com.example.common.Result;
import com.example.entity.Collect;
import com.example.entity.Comment;
import com.example.entity.Introduction;
import com.example.service.CollectService;
import com.example.service.CommentService;
import com.example.service.IntroductionService;
import com.github.pagehelper.PageInfo;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.List;

/**
 * 攻略信息表前端操作接口
 **/
@RestController
@RequestMapping("/introduction")
public class IntroductionController {

    @Resource
    private IntroductionService introductionService;
    @Resource
    private CollectService collectService;
    @Resource
    private CommentService commentService;

    /**
     * 新增
     */
    @PostMapping("/add")
    public Result add(@RequestBody Introduction introduction) {
        introductionService.add(introduction);
        return Result.success();
    }

    /**
     * 删除
     */
    @DeleteMapping("/delete/{id}")
    public Result deleteById(@PathVariable Integer id) {
        introductionService.deleteById(id);
        return Result.success();
    }

    /**
     * 批量删除
     */
    @DeleteMapping("/delete/batch")
    public Result deleteBatch(@RequestBody List<Integer> ids) {
        introductionService.deleteBatch(ids);
        return Result.success();
    }

    /**
     * 修改
     */
    @PutMapping("/update")
    public Result updateById(@RequestBody Introduction introduction) {
        introductionService.updateById(introduction);
        return Result.success();
    }

    /**
     * 根据ID查询
     */
    @GetMapping("/selectById/{id}")
    public Result selectById(@PathVariable Integer id) {
        Introduction introduction = introductionService.selectById(id);
        return Result.success(introduction);
    }

    @GetMapping("/selectNew4")
    public Result selectNew4() {
        List<Introduction> list = introductionService.selectNew4();
        return Result.success(list);
    }

    /**
     * 查询所有
     */
    @GetMapping("/selectAll")
    public Result selectAll(Introduction introduction ) {
        List<Introduction> list = introductionService.selectAll(introduction);
        return Result.success(list);
    }

    /**
     * 分页查询
     */
    @GetMapping("/selectPage")
    public Result selectPage(Introduction introduction,
                             @RequestParam(defaultValue = "1") Integer pageNum,
                             @RequestParam(defaultValue = "10") Integer pageSize) {
        PageInfo<Introduction> page = introductionService.selectPage(introduction, pageNum, pageSize);
        return Result.success(page);
    }





    /**
     * 点赞
     */
    @PostMapping("/likePost")
    public Result likePost(@RequestBody Collect collect) {
        Integer introductionId = collect.getIntroductionId();
        Introduction introduction = introductionService.selectById(introductionId);
        introduction.setCollect(introduction.getCollect() + 1);
        introductionService.updateById(introduction);
        collectService.add(collect);
        return Result.success();
    }
    /**
     * 取消点赞
     */
    @DeleteMapping("/unlikePost")
    public Result unlikePost(@RequestBody Collect collect) {
        Integer introductionId = collect.getIntroductionId();
        Integer userId = collect.getUserId();
        Introduction introduction = introductionService.selectById(introductionId);
        introduction.setCollect(introduction.getCollect() - 1);
        introductionService.updateById(introduction);

        Collect select = collectService.select(introductionId, userId);
        collectService.deleteById(select.getId());
        return Result.success();
    }
    /**
     * 评论
     */
    @PostMapping("/comment")
    public Result comment(@RequestBody Comment comment) {
        Integer introductionId = comment.getIntroductionId();
        Introduction introduction = introductionService.selectById(introductionId);
        introduction.setComment(introduction.getComment() + 1);
        introductionService.updateById(introduction);
        commentService.add(comment);
        return Result.success();
    }
    /**
     * 用户端分页查询，因为需要考虑用户对于博客是否点赞
     */
    @GetMapping("/selectPageByUser")
    public Result selectPageByUser(Introduction introduction,
                             @RequestParam(defaultValue = "1") Integer pageNum,
                             @RequestParam(defaultValue = "10") Integer pageSize) {
        PageInfo<Introduction> page = introductionService.selectPageByUser(introduction, pageNum, pageSize);
        return Result.success(page);
    }
    /**
     * 用户端根据ID查询
     */
    @GetMapping("/selectByIdByUser/{id}")
    public Result selectByIdByUser(@PathVariable Integer id) {
        Introduction introduction = introductionService.selectByIdByUser(id);
        return Result.success(introduction);
    }
}