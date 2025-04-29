package com.example.service;

import cn.hutool.core.date.DateUtil;
import cn.hutool.core.util.ObjectUtil;
import cn.hutool.http.HtmlUtil;
import com.example.context.BaseContext;
import com.example.entity.Collect;
import com.example.entity.Comment;
import com.example.entity.Introduction;
import com.example.entity.User;
import com.example.mapper.CollectMapper;
import com.example.mapper.CommentMapper;
import com.example.mapper.IntroductionMapper;
import com.example.mapper.UserMapper;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 攻略信息表业务处理
 **/
@Service
public class IntroductionService {

    @Resource
    private IntroductionMapper introductionMapper;
    @Resource
    private UserMapper userMapper;
    @Resource
    private CommentMapper commentMapper;
    @Resource
    private CollectMapper collectMapper;

    /**
     * 新增
     */
    public void add(Introduction introduction) {
        introduction.setTime(DateUtil.now());
        if (introduction.getImg() == null || introduction.getImg().isEmpty()){
            introduction.setImg("http://localhost:9090/files/1742016321587-1697438073596-avatar.png");
        }
        introductionMapper.insert(introduction);
    }

    /**
     * 删除
     */
    public void deleteById(Integer id) {
        introductionMapper.deleteById(id);
    }

    /**
     * 批量删除
     */
    public void deleteBatch(List<Integer> ids) {
        for (Integer id : ids) {
            introductionMapper.deleteById(id);
        }
    }

    /**
     * 修改
     */
    public void updateById(Introduction introduction) {
        introductionMapper.updateById(introduction);
    }

    /**
     * 根据ID查询
     */
    public Introduction selectById(Integer id) {
        Introduction introduction = introductionMapper.selectById(id);
        User user = userMapper.selectById(introduction.getUserId());
        if (ObjectUtil.isNotEmpty(user)) {
            introduction.setUserName(user.getUsername());
        }
        return introduction;
    }

    /**
     * 查询所有
     */
    public List<Introduction> selectAll(Introduction introduction) {
        return introductionMapper.selectAll(introduction);
    }

    /**
     * 分页查询
     */
    public PageInfo<Introduction> selectPage(Introduction introduction, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum, pageSize);
        List<Introduction> list = introductionMapper.selectAll(introduction);
        for (Introduction dbIntroduction : list) {
            // 把富文本内容去标签
            dbIntroduction.setDescription(HtmlUtil.cleanHtmlTag(dbIntroduction.getContent()));
        }
        return PageInfo.of(list);
    }

    public List<Introduction> selectNew4() {
        return introductionMapper.selectNew4();
    }




    /**
     * 用户端分页查询，因为需要考虑用户对于博客是否点赞
     */
    public PageInfo<Introduction> selectPageByUser(Introduction introduction, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum, pageSize);
        List<Introduction> list = introductionMapper.selectAll(introduction);
        for (Introduction dbIntroduction : list) {
            // 把富文本内容去标签
            dbIntroduction.setDescription(HtmlUtil.cleanHtmlTag(dbIntroduction.getContent()));
        }

        //对用户点赞的博客进行标记
        //获取用户点赞的博客
        Long currentId = BaseContext.getCurrentId();
        Collect collect = new Collect();
        collect.setUserId(Math.toIntExact(currentId));
        List<Collect> collects = collectMapper.selectAll(collect);

        // 创建一个 Map，用于存储 Introduction 的 id 和对应的 Introduction 对象
        Map<Integer, Introduction> introMap = new HashMap<>();
        for (Introduction intro : list) {
            intro.setCollected(0); // 初始化为 false
            introMap.put(intro.getId(), intro); // 将 Introduction 对象存入 Map
        }

        // 遍历 collects，直接通过 Map 获取对应的 Introduction 对象并设置为 true
        for (Collect c : collects) {
            Integer introductionId = c.getIntroductionId();
            Introduction intro = introMap.get(introductionId);
            if (intro != null) {
                intro.setCollected(1);
            }
        }
        return PageInfo.of(list);
    }
    /**
     * 用户端根据ID查询，因为需要考虑用户对于博客是否点赞,还要拼接评论区
     */
    public Introduction selectByIdByUser(Integer id) {
        Introduction introduction = introductionMapper.selectById(id);
        User user = userMapper.selectById(introduction.getUserId());
        if (ObjectUtil.isNotEmpty(user)) {
            introduction.setUserName(user.getUsername());
        }

        //拼接评论区
        Comment comment = new Comment();
        comment.setIntroductionId(id);
        List<Comment> comments = commentMapper.selectAll(comment);
        introduction.setComments(comments);

        //对用户点赞的博客进行标记
        Long currentId = BaseContext.getCurrentId();
        Collect collect = new Collect();
        collect.setUserId(Math.toIntExact(currentId));
        collect.setIntroductionId(id);
        List<Collect> collects = collectMapper.selectAll(collect);
        if (ObjectUtil.isNotEmpty(collects)) {
            introduction.setCollected(1);
        } else {
            introduction.setCollected(0);
        }
        return introduction;
    }
}