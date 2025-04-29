package com.example.service.impl;

import com.example.DAO.CheckinCountDTO;
import com.example.common.enums.BadgeStandardTypeEnum;
import com.example.context.BaseContext;
import com.example.entity.*;
import com.example.mapper.BadgeStandardMapper;
import com.example.mapper.ExerciseCheckinMapper;
import com.example.mapper.ExerciseMapper;
import com.example.mapper.UserBasicInfoMapper;
import com.example.service.ExerciseService;
import com.example.utils.ExerciseRecommendation;
import com.example.utils.MedalConstants;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.*;

/**
 * 运动信息业务处理
 */
@Service
public class ExerciseServiceImpl implements ExerciseService {

    @Autowired
    private ExerciseMapper exerciseMapper;
    @Autowired
    private ExerciseCheckinMapper exerciseCheckinMapper;

    @Autowired
    private UserBasicInfoMapper userBasicInfoMapper;
    @Autowired
    private BadgeStandardMapper badgeStandardMapper;



    // 勋章检测
    public void checkMedal(Double addCal) {
        int[] sportAdd = MedalConstants.SPORT_ADD_DAYS;
        int[] sportContinue = MedalConstants.SPORT_CONTINUE_DAYS;
        int[] sportCal = MedalConstants.SPORT_CALORIE_THRESHOLD;
        Long userId = BaseContext.getCurrentId();
        UserCheckInfo userCheckInfo = userBasicInfoMapper.selectCheckInfoById(userId);
        CheckinCountDTO checkinCountDTO = exerciseCheckinMapper.selectCheckinCounts(userId);
        Integer medalDay;

        // 运动累计打卡勋章检查
        if(checkinCountDTO.getTodayCount() == 0){
            Integer addDay = userCheckInfo.getSportAddDay();
            userCheckInfo.setSportAddDay(addDay+1);
            medalDay = 0;
            for(int i = 0 ; i < sportAdd.length ; i++){
                if(sportAdd[i] == addDay+1){
                    medalDay = sportAdd[i];
                }else if(sportAdd[i] > addDay+1){
                    break;
                }else{
                    continue;
                }
            }
            if(medalDay > 0){
                Integer badgeId = badgeStandardMapper.selectIdByTypeAndDays(BadgeStandardTypeEnum.运动打卡天数.name(), medalDay);
                MyBadge myBadge = new MyBadge(userId, badgeId, true);
                badgeStandardMapper.insertPersonBadge(myBadge);
            }
        }

        //运动连续打卡勋章检查
        if(checkinCountDTO.getYesterdayCount() > 0 && checkinCountDTO.getTodayCount() == 0){
            Integer continueDay = userCheckInfo.getSportContinueDay();
            userCheckInfo.setSportContinueDay(continueDay+1);
            medalDay = 0;
            for(int i = 0 ; i < sportContinue.length ; i++){
                if(sportContinue[i] == continueDay+1){
                    medalDay = sportContinue[i];
                }else if(sportContinue[i] > continueDay+1){
                    break;
                }else{
                    continue;
                }
            }
            if(medalDay > 0){
                Integer badgeId = badgeStandardMapper.selectIdByTypeAndDays(BadgeStandardTypeEnum.运动连续打卡天数.name(), medalDay);
                MyBadge myBadge = new MyBadge(userId, badgeId, true);
                badgeStandardMapper.insertPersonBadge(myBadge);
            }
        }

        // 总卡路里燃烧勋章检查
        Double cal = userCheckInfo.getAddSportCal();
        Double calNew = cal + addCal;
        userCheckInfo.setAddSportCal(calNew);
        medalDay = 0;
        for(int i = 0 ; i < sportCal.length ; i++){
            if(sportCal[i] > cal && sportCal[i] <= calNew){
                medalDay = sportCal[i];
            }else if(sportCal[i] > calNew){
                break;
            }else{
                continue;
            }
        }
        if(medalDay > 0){
            Integer badgeId = badgeStandardMapper.selectIdByTypeAndDays(BadgeStandardTypeEnum.运动记录消耗.name(), medalDay);
            MyBadge myBadge = new MyBadge(userId, badgeId, true);
            badgeStandardMapper.insertPersonBadge(myBadge);
        }

        userBasicInfoMapper.updateCheckInfo(userCheckInfo);

    }

    @Override
    public Map<String, ArrayList<Exercise>> simpleSelect() {
        List<Exercise> exercises = exerciseMapper.selectAll(new Exercise());
        Map<String, ArrayList<Exercise>> exerciseMap = new HashMap<>();
        //格式：运动类型：【相关运动】
        for (Exercise exercise : exercises) {
            if (!exerciseMap.containsKey(exercise.getExerciseCategory())) {
                exerciseMap.put(exercise.getExerciseCategory(), new ArrayList<>());
            }
            exerciseMap.get(exercise.getExerciseCategory()).add(exercise);
        }
        return exerciseMap;
    }

    @Override
    public Map<String, ArrayList<ExerciseCheckin>> selectHistory(String month) {
        Long userId = BaseContext.getCurrentId();
        List<ExerciseCheckin> exerciseCheckins = exerciseCheckinMapper.selectHistory(userId);
        LocalDate startDate = LocalDate.parse(month);
        LocalDate endDate = startDate.plusMonths(1);
        Map<String, ArrayList<ExerciseCheckin>> resultMap = new HashMap<>();
        for (ExerciseCheckin exerciseCheckin : exerciseCheckins) {
            LocalDate date = exerciseCheckin.getCreateTime().toLocalDate();
            if (date.isBefore(startDate) || date.isAfter(endDate)){
                continue;
            }
            if (!resultMap.containsKey(date.toString())){
                resultMap.put(date.toString(), new ArrayList<>());
            }
            resultMap.get(date.toString()).add(exerciseCheckin);
        }
        return resultMap;
    }

    @Override
    public List<ExerciseCheckin> selectRecommend(Integer expectedCalories) {
        Long userId = BaseContext.getCurrentId();
//        List<ExerciseCheckin> exerciseCheckins = exerciseMapper.selectHistory(userId);
        //先检查数据库中是否有推荐的运动
        Map map = new HashMap<>();
        map.put("userId", userId);
        map.put("createDate", LocalDate.now());
        List<ExerciseCheckin> exerciseCheckins = exerciseCheckinMapper.selectAll(map);

        if (exerciseCheckins.isEmpty()) {
            //推荐运动
            List<Exercise> exercises = exerciseMapper.selectAll(new Exercise());
            ExerciseRecommendation recommendation = new ExerciseRecommendation(exercises);
            List<ExerciseRecommend> recommendExercises = recommendation.recommendExercises(expectedCalories);

            //记录这些今日推荐运动
            List<Map> list = new ArrayList<>();
            for (ExerciseRecommend exercise : recommendExercises) {
                Map temp = new HashMap<>();
                temp.put("userId", userId);
                temp.put("now", LocalDateTime.now());
                temp.put("exerciseId", exercise.getExerciseId());
                temp.put("exerciseName", exercise.getExerciseName());
                temp.put("duration", exercise.getDuration());
                temp.put("caloriesBurned", exercise.getDuration() * exercise.getCaloriesBurnRate() / 10);//每10分钟
                list.add(temp);
            }
            exerciseCheckinMapper.insertBatch(list);

            //重新查询
            exerciseCheckins = exerciseCheckinMapper.selectAll(map);
        }
        return exerciseCheckins;
    }

    @Override
    public void addNewToday(ExerciseRecommend exercise) {
        List<Map> list = new ArrayList<>();
        Map temp = new HashMap<>();
        temp.put("userId", BaseContext.getCurrentId());
        temp.put("now", LocalDateTime.now());
        temp.put("exerciseId", exercise.getExerciseId());
        temp.put("exerciseName", exercise.getExerciseName());
        temp.put("duration", exercise.getDuration());
        temp.put("caloriesBurned", exercise.getDuration() * exercise.getCaloriesBurnRate() / 10);//每10分钟
        list.add(temp);
        exerciseCheckinMapper.insertBatch(list);
    }

    @Override
    @Transactional
    public void checkin(Integer checkinId, Integer feedback) {
        //更新数据
        ExerciseCheckin exerciseCheckin = exerciseCheckinMapper.selectById(Long.valueOf(checkinId));
        exerciseCheckin.setFeedback(feedback);
        exerciseCheckin.setCheckinDate(LocalDateTime.now());

        //计算卡路里消耗
        Exercise exercise = exerciseMapper.selectById(exerciseCheckin.getExerciseId());
        Integer caloriesBurned = exercise.getCaloriesBurnRate() * exerciseCheckin.getDuration() / 10;//每10分钟
        exerciseCheckin.setCaloriesBurned(caloriesBurned);
        Double addCal = (double) caloriesBurned;
        this.checkMedal(addCal);

        //打卡今日运动
        exerciseCheckinMapper.updateById(exerciseCheckin);
    }

    /**
     * 新增
     */
    public void add(Exercise exercise) {
        // 如果需要记录创建时间或创建人，可以在此处补充
        exerciseMapper.insert(exercise);
    }

    /**
     * 删除
     */
    public void deleteById(Integer id) {
        exerciseMapper.deleteById(id);
    }

    /**
     * 批量删除
     */
    public void deleteBatch(List<Integer> ids) {
        for (Integer id : ids) {
            exerciseMapper.deleteById(id);
        }
    }

    /**
     * 修改
     */
    public void updateById(Exercise exercise) {
        exerciseMapper.updateById(exercise);
    }

    /**
     * 根据ID查询
     */
    public Exercise selectById(Integer id) {
        return exerciseMapper.selectById(id);
    }

    /**
     * 查询所有
     */
    public List<Exercise> selectAll(Exercise exercise) {
        return exerciseMapper.selectAll(exercise);
    }

    /**
     * 分页查询
     */
    public PageInfo<Exercise> selectPage(Exercise exercise, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum, pageSize);
        List<Exercise> list = exerciseMapper.selectAll(exercise);
        return PageInfo.of(list);
    }

}
