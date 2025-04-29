package com.example.service;

import com.example.context.BaseContext;
import com.example.entity.BadgeStandard;
import com.example.mapper.BadgeStandardMapper;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.stereotype.Service;
import javax.annotation.Resource;
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;

@Service
public class BadgeStandardService {

    @Resource
    private BadgeStandardMapper badgeStandardMapper;

    public void add(BadgeStandard badgeStandard) {
        badgeStandardMapper.insert(badgeStandard);
    }

    public void deleteById(Integer id) {
        badgeStandardMapper.deleteById(id);
    }

    public void updateById(BadgeStandard badgeStandard) {
        badgeStandardMapper.updateById(badgeStandard);
    }

    public BadgeStandard selectById(Integer id) {
        return badgeStandardMapper.selectById(id);
    }

    public List<BadgeStandard> selectAll(BadgeStandard condition) {
        return badgeStandardMapper.selectAll(condition);
    }

    public List<BadgeStandard> selectEarnedNewBadges() {
        List<BadgeStandard> bs = new ArrayList<>();
        Long userId = BaseContext.getCurrentId();
        bs = badgeStandardMapper.selectEarnedNewBadges(userId);
        for(int i = 0 ; i < bs.size() ; i++){
            BadgeStandard badgeStandard = bs.get(i);
            badgeStandardMapper.updatePersonBadge(userId, badgeStandard.getId());
        }
        return bs;
    }

    public PageInfo<BadgeStandard> selectPage(BadgeStandard condition, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum, pageSize);
        List<BadgeStandard> list = badgeStandardMapper.selectAll(condition);
        return PageInfo.of(list);
    }
    public Map<String, ArrayList<BadgeStandard>> selectByUserId(){
        Long userId = BaseContext.getCurrentId();
        //已有勋章列表
        ArrayList<BadgeStandard> bsEarned = badgeStandardMapper.selectEarnedBadges(userId);
        //未有勋章列表
        ArrayList<BadgeStandard> bsUnowned = badgeStandardMapper.selectUnownedBadges(userId);
        // 构建返回Map（使用接口类型更规范）
        Map<String, ArrayList<BadgeStandard>> result = new HashMap<>(2);

        // 类型转换（需确保MyBatis返回的是ArrayList）
        result.put("earned", bsEarned);
        result.put("unowned", bsUnowned);

        return result;
    }
}