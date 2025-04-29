package com.example.service;

import cn.hutool.core.collection.CollectionUtil;
import cn.hutool.http.HtmlUtil;
import com.example.entity.Collect;
import com.example.exception.CustomException;
import com.example.mapper.CollectMapper;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

/**
 * 收藏信息表业务处理
 **/
@Service
public class CollectService {

    @Resource
    private CollectMapper collectMapper;

    /**
     * 新增
     */
    public void add(Collect collect) {
        // 先去判断一下该用户有没有收藏过该攻略
        List<Collect> collects = collectMapper.selectAll(collect);
        if (CollectionUtil.isNotEmpty(collects)) {
            throw new CustomException("-1", "您已经收藏过该攻略，请勿重复收藏");
        }
        collectMapper.insert(collect);
    }

    /**
     * 删除
     */
    public void deleteById(Integer id) {
        collectMapper.deleteById(id);
    }

    /**
     * 批量删除
     */
    public void deleteBatch(List<Integer> ids) {
        for (Integer id : ids) {
            collectMapper.deleteById(id);
        }
    }

    /**
     * 修改
     */
    public void updateById(Collect collect) {
        collectMapper.updateById(collect);
    }

    /**
     * 根据ID查询
     */
    public Collect selectById(Integer id) {
        return collectMapper.selectById(id);
    }

    /**
     * 条件查询
     */
    public Collect select(Integer introductionId, Integer userId) {
        Collect collect = new Collect();
        collect.setIntroductionId(introductionId);
        collect.setUserId(userId);
        return collectMapper.selectAll(collect).get(0);
    }

    /**
     * 查询所有
     */
    public List<Collect> selectAll(Collect collect) {
        return collectMapper.selectAll(collect);
    }

    /**
     * 分页查询
     */
    public PageInfo<Collect> selectPage(Collect collect, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum, pageSize);
        List<Collect> list = collectMapper.selectAll(collect);
        for (Collect dbCollect : list) {
            dbCollect.setDescription(HtmlUtil.cleanHtmlTag(dbCollect.getContent()));
        }
        return PageInfo.of(list);
    }

}