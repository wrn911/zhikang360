package com.example.service;

import com.example.DAO.FoodInfoDAO;
import com.example.DAO.IllnessInfoDAO;
import com.example.DAO.SleepInfoDAO;
import com.example.DAO.SportInfoDAO;
import com.example.context.BaseContext;
import com.example.entity.*;
import com.example.mapper.*;
import com.example.utils.*;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.stereotype.Service;
import javax.annotation.Resource;
import java.time.LocalDateTime;
import java.util.List;

@Service
public class UserBasicInfoService {

    @Resource
    private UserBasicInfoMapper userBasicInfoMapper;
    @Resource
    private FoodInfoMapper foodInfoMapper;
    @Resource
    private SportInfoMapper sportInfoMapper;
    @Resource
    private SleepInfoMapper sleepInfoMapper;
    @Resource
    private IllnessInfoMapper illnessInfoMapper;

    public void add(UserBasicInfo userBasicInfo) {

        userBasicInfoMapper.insert(userBasicInfo);
    }

    public void deleteById(Integer userId) {

        userBasicInfoMapper.deleteById(userId);
    }

    public void updateById(UserBasicInfo userBasicInfo) {
        Long userId = BaseContext.getCurrentId();
        userBasicInfo.setUserId(userId);
        userBasicInfoMapper.updateById(userBasicInfo);
    }


    public UserBasicInfo selectById(Integer userId) {

        return userBasicInfoMapper.selectById(userId);
    }

    public List<UserBasicInfo> selectAll(UserBasicInfo condition) {

        return userBasicInfoMapper.selectAll(condition);
    }

    public PageInfo<UserBasicInfo> selectPage(UserBasicInfo condition, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum, pageSize);
        List<UserBasicInfo> list = userBasicInfoMapper.selectAll(condition);
        return PageInfo.of(list);
    }

    public void addFoodInfo(FoodInfoDAO foodInfoDAO) {
        FoodInfo foodInfo = new FoodInfo();
        Long userId = BaseContext.getCurrentId();
        foodInfo.setUserId(userId);
        foodInfo.setWillingness(foodInfoDAO.getWillingness());
        ListUtils listUtils = new ListUtils();
        foodInfo.setPreferences(listUtils.joinWithDun(foodInfoDAO.getPreferences(),true,"暂无请忽略"));
        foodInfo.setAvoids(listUtils.joinWithDun(foodInfoDAO.getAvoids(),true,"暂无请忽略"));
        LocalDateTime time = LocalDateTime.now();
        foodInfo.setCreateTime(time);
        foodInfo.setUpdateTime(time);
        foodInfoMapper.insert(foodInfo);
    }

    public void updateFoodInfoById(FoodInfo foodInfo) {
        Long userId = BaseContext.getCurrentId();
        foodInfo.setUserId(userId);
        foodInfoMapper.updateById(foodInfo);
    }

    public FoodInfo selectFoodInfoById() {
        Long userId = BaseContext.getCurrentId();
        return foodInfoMapper.selectByUserId(userId);
    }

    public void addSportInfo(SportInfoDAO sportInfoDAO) {
        Long userId = BaseContext.getCurrentId();
        ListUtils listUtils = new ListUtils();
        SportInfo sportInfo = new SportInfo();
        LocalDateTime time = LocalDateTime.now();
        sportInfo.setUserId(userId);
        sportInfo.setWillingness(sportInfoDAO.getWillingness());
        sportInfo.setPreferences(sportInfoDAO.getPreferences());
        sportInfo.setExperience(sportInfoDAO.getExperience());
        sportInfo.setWeaknesses(sportInfoDAO.getWeaknesses());
        sportInfo.setIntensity(sportInfoDAO.getIntensity());
        sportInfo.setFreeTimes(listUtils.joinWithDun(sportInfoDAO.getFreeTime(), true, "暂无请忽略"));
        sportInfo.setCreateTime(time);
        sportInfo.setUpdateTime(time);
        sportInfoMapper.insert(sportInfo);
    }

    public void updateSportInfoById(SportInfo sportInfo) {
        Long userId = BaseContext.getCurrentId();
        sportInfo.setUserId(userId);
        sportInfoMapper.updateById(sportInfo);
    }

    public void addSleepInfo(SleepInfoDAO sleepInfoDAO) {
        Long userId = BaseContext.getCurrentId();
        ListUtils listUtils = new ListUtils();
        SleepInfo sleepInfo = new SleepInfo();
        LocalDateTime time = LocalDateTime.now();
        sleepInfo.setUserId(userId);
        sleepInfo.setSleepTime(sleepInfoDAO.getSleepTime());
        sleepInfo.setWakeupTime(sleepInfoDAO.getWakeupTime());
        sleepInfo.setEmotions(listUtils.joinWithDun(sleepInfoDAO.getEmotions(), true, "暂无请忽略"));
        sleepInfo.setCreateTime(time);
        sleepInfo.setUpdateTime(time);
        sleepInfoMapper.insert(sleepInfo);
    }

    public void updateSleepInfoById(SleepInfo sleepInfo) {
        Long userId = BaseContext.getCurrentId();
        sleepInfo.setUserId(userId);
        sleepInfoMapper.updateById(sleepInfo);
    }

    public void addIllnessInfo(IllnessInfoDAO illnessInfoDAO) {
        Long userId = BaseContext.getCurrentId();
        ListUtils listUtils = new ListUtils();
        IllnessInfo illnessInfo = new IllnessInfo();
        LocalDateTime time = LocalDateTime.now();
        illnessInfo.setUserId(userId);
        illnessInfo.setAllergyType(illnessInfoDAO.getAllergy().getType());
        illnessInfo.setAllergyDetails(listUtils.joinWithDun(illnessInfoDAO.getAllergy().getDetails(),true, "暂无请忽略"));
        illnessInfo.setChronicDiseases(listUtils.joinWithDun(illnessInfoDAO.getChronicDiseases(),true, "暂无请忽略"));
        illnessInfo.setHealthIssues(illnessInfoDAO.getHealthIssues());
        illnessInfo.setCreateTime(time);
        illnessInfo.setUpdateTime(time);
        illnessInfoMapper.insert(illnessInfo);
    }

    public void updateIllnessInfoById(IllnessInfo illnessInfo) {
        Long userId = BaseContext.getCurrentId();
        illnessInfo.setUserId(userId);
        illnessInfoMapper.updateById(illnessInfo);
    }

    public IllnessInfo selectIllnessInfoById() {
        Long userId = BaseContext.getCurrentId();
        return illnessInfoMapper.selectByUserId(userId);
    }

    public SleepInfo selectSleepInfoById() {
        Long userId = BaseContext.getCurrentId();
        return sleepInfoMapper.selectByUserId(userId);
    }

    public SportInfo selectSportInfoById() {
        Long userId = BaseContext.getCurrentId();
        return sportInfoMapper.selectByUserId(userId);
    }
}