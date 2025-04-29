package com.example.mapper;

import com.example.entity.Introduction;
import org.apache.ibatis.annotations.Select;

import java.util.List;

/**
 * 操作introduction相关数据接口
*/
public interface IntroductionMapper {

    /**
      * 新增
    */
    int insert(Introduction introduction);

    /**
      * 删除
    */
    int deleteById(Integer id);

    /**
      * 修改
    */
    int updateById(Introduction introduction);

    /**
      * 根据ID查询
    */
    Introduction selectById(Integer id);

    /**
      * 查询所有
    */
    List<Introduction> selectAll(Introduction introduction);

    @Select("select * from introduction order by id desc limit 4")
    List<Introduction> selectNew4();
}