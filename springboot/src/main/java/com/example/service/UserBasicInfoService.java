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
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import javax.annotation.Resource;
import java.time.*;
import java.util.Date;
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
    @Resource
    private ExerciseCheckinMapper exerciseCheckinMapper;

    @Resource
    private UserRecommendInfoMapper userRecommendInfoMapper;
    @Autowired
    private FoodRecommendMapper foodRecommendMapper;

    public void add(UserBasicInfo userBasicInfo) {
        userBasicInfoMapper.insert(userBasicInfo);
    }

    public UserRecommendInfo selectRecommend(){
        Long userId = BaseContext.getCurrentId();
        return userRecommendInfoMapper.selectByUserId(userId);
    }

    public void deleteById(Integer userId) {

        userBasicInfoMapper.deleteById(userId);
    }

    private int calculateAge(Date birthDate) {
        if (birthDate == null) return 30; // 默认值（可以根据需要调整）
        LocalDate birth = birthDate.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();
        return Period.between(birth, LocalDate.now()).getYears();
    }


    public void updateById(UserBasicInfo userBasicInfo1) {
        Long userId = BaseContext.getCurrentId();
        UserBasicInfo userBasicInfo = userBasicInfoMapper.selectById((int)(long)userId);
        if ("男".equals(userBasicInfo1.getGender()) || "女".equals(userBasicInfo1.getGender()) || "保密".equals(userBasicInfo1.getGender())) {
            userBasicInfo.setGender(userBasicInfo1.getGender());
        }
        BeanUtils.copyProperties(userBasicInfo1, userBasicInfo);
        userBasicInfo.setUserId(userId);
        UserRecommendInfo userRecommendInfo = userRecommendInfoMapper.selectByUserId(userId);
        // 获取基础数据
        int height = (int) userBasicInfo.getHeight(); // cm
        int weight = (int)userBasicInfo.getWeight(); // kg
        int age = calculateAge(userBasicInfo.getBirthDate());
        String gender = userBasicInfo.getGender(); // "男" 或 "女"
        // 计算 BMR（基础代谢率）
        double bmr;
        if ("女".equals(gender)) {
            bmr = 10 * weight + 6.25 * height - 5 * age - 161;
        } else {
            bmr = 10 * weight + 6.25 * height - 5 * age + 5;
        }
        // 估算活动系数（默认中等活动）
        int tdee = (int)(bmr * 1.35);
        tdee = tdee / 100 * 100;
        // 推荐运动消耗 = 体重 × 系数（比如 6）
        int exerciseCalories = weight * 6;
        if(userRecommendInfo == null){
            userRecommendInfo = new UserRecommendInfo();
            userRecommendInfo.setUserId(userId);
            userRecommendInfo.setSleepTimeStart(LocalTime.of(22, 0));
            userRecommendInfo.setSleepTimeEnd(LocalTime.of(6, 0));
            userRecommendInfo.setSleepTimeInmid(LocalTime.of(13, 0));
            // 写入推荐信息
            userRecommendInfo.setFoodCalories(tdee);
            userRecommendInfo.setExerciseCalories(exerciseCalories);
            userRecommendInfoMapper.insert(userRecommendInfo);
        }else{
            // 写入推荐信息
            userRecommendInfo.setFoodCalories((int) Math.round(tdee));
            userRecommendInfo.setExerciseCalories((int) Math.round(exerciseCalories));
            userRecommendInfoMapper.update(userRecommendInfo);
        }
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
        foodInfo.setAim(foodInfoDAO.getAim());
        foodInfo.setWillingness(foodInfoDAO.getWillingness());
        ListUtils listUtils = new ListUtils();
        foodInfo.setPreferences(listUtils.joinWithDun(foodInfoDAO.getPreferences(),true,"暂无请忽略"));
        foodInfo.setAvoids(listUtils.joinWithDun(foodInfoDAO.getAvoids(),true,"暂无请忽略"));
        LocalDateTime time = LocalDateTime.now();
        foodInfo.setCreateTime(time);
        foodInfo.setUpdateTime(time);
        foodInfoMapper.insert(foodInfo);
        foodRecommendMapper.insertUserFoodRecommendFromTemplate(userId);
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
        exerciseCheckinMapper.insertUserExerciseRecommendFromTemplate(userId);
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