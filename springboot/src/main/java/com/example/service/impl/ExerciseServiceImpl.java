package com.example.service.impl;

import com.example.DAO.CheckinCountDTO;
import com.example.common.enums.BadgeStandardTypeEnum;
import com.example.common.enums.ExerciseCategoryEnum;
import com.example.common.enums.FoodGroceryEnum;
import com.example.common.enums.FoodTimeEnum;
import com.example.context.BaseContext;
import com.example.entity.*;
import com.example.mapper.*;
import com.example.service.ExerciseService;
import com.example.utils.ExerciseRecommendation;
import com.example.utils.MedalConstants;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
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

    @Autowired
    private UserRecommendInfoMapper userRecommendInfoMapper;

    public void blockChainLink(int x){
        Process proc;
        x=x-2;
        try {
            // 指定虚拟环境中的 Python 解释器路径
            // 指定虚拟环境中的 Python 解释器路径
            String pythonExecutable = "E:\\ruanjian2\\anaconda\\envs\\NanoGPT\\python.exe";  // 7层上级目录
            String scriptPath = "D:\\Java\\IdeaProjects\\zhikang360\\pythonProject2\\main"+x+".py";  // 7层上级目录

            // 运行 Python 脚本
            proc = Runtime.getRuntime().exec(pythonExecutable + " " + scriptPath);

            // 读取标准输出流
            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            String line;
            while ((line = in.readLine()) != null) {
                System.out.println("Output: " + line);
            }
            in.close();

            // 读取标准错误流
            BufferedReader errorIn = new BufferedReader(new InputStreamReader(proc.getErrorStream()));
            while ((line = errorIn.readLine()) != null) {
                System.err.println("Error: " + line);
            }
            errorIn.close();

            // 等待 Python 进程执行完毕
            proc.waitFor();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

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
                blockChainLink(badgeId);
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
                blockChainLink(badgeId);
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
            blockChainLink(badgeId);
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
        /*
        * if (exerciseCheckins.isEmpty()) {
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
        *
        *
        * */

        return exerciseCheckins;
    }

    @Override
    public void generateRecommend() {
        Long userId = BaseContext.getCurrentId();
        UserRecommendInfo userRecommendInfo = userRecommendInfoMapper.selectByUserId(userId);
        int recommendCalories = userRecommendInfo.getExerciseCalories();
        List<ExerciseRecommend> recommendExercises = new ArrayList<>();
        recommendExercises.add(this.recommendExercises(ExerciseCategoryEnum.有氧运动.name(), (int)(recommendCalories * 0.5), userId));
        recommendExercises.add(this.recommendExercises(ExerciseCategoryEnum.力量训练.name(), (int)(recommendCalories * 0.2), userId));
        recommendExercises.add(this.recommendExercises(ExerciseCategoryEnum.getRandomCategory().name(), (int)(recommendCalories * 0.3), userId));
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
    }

    public ExerciseRecommend recommendExercises(String type, int targetCalories, Long userId) {
        // 获取某类运动的候选推荐列表
        List<UserExerciseRecommendList> exerciseRecommendLists = exerciseCheckinMapper.selectByCategory(userId, type);

        // 利用轮盘赌抽选推荐
        ExerciseRecommend recommend = buildRecommend(exerciseRecommendLists, targetCalories);

        return recommend;
    }

    private ExerciseRecommend buildRecommend(List<UserExerciseRecommendList> candidates, int targetCalories) {
        if (candidates == null || candidates.isEmpty()) {
            throw new IllegalArgumentException("该类型下无可用运动项目");
        }

        // 构建轮盘赌的权重数组（仅用 weight 字段）
        List<Double> weights = new ArrayList<>();
        double totalWeight = 0.0;

        for (UserExerciseRecommendList e : candidates) {
            double w = e.getWeight(); // 注意：weight 为 double 类型，越大越容易被选中
            weights.add(w);
            totalWeight += w;
        }

        // 抽取一个随机数
        double rand = Math.random() * totalWeight;

        // 执行轮盘赌选择
        int selectedIndex = 0;
        double sum = 0;
        for (int i = 0; i < weights.size(); i++) {
            sum += weights.get(i);
            if (rand <= sum) {
                selectedIndex = i;
                break;
            }
        }

        // 获取被选中的运动项目
        UserExerciseRecommendList selected = candidates.get(selectedIndex);

        // 使用 calories_burn_rate（每10分钟消耗）计算所需时长（分钟）
        int burnPer10Min = Integer.parseInt(selected.getCaloriesBurnRate());
        int duration = (int) Math.round(targetCalories * 10.0 / burnPer10Min);

        // 将时长四舍五入为最接近的5的倍数
        int roundedDuration = ((int) Math.round(duration / 5.0) + 1) * 5;

        // 构造推荐结果
        ExerciseRecommend result = new ExerciseRecommend();
        result.setExerciseId(selected.getExerciseId());
        result.setExerciseName(selected.getExerciseName());
        result.setExerciseCategory(selected.getExerciseCategory());
        result.setCaloriesBurnRate(burnPer10Min);
        result.setCalories(targetCalories);
        result.setDuration(roundedDuration);

        return result;
    }
    @Override
    public List<UserExerciseRecommendList> GetUserExerciseRecommendList(){
        Long userId = BaseContext.getCurrentId();
        LocalDate date = LocalDate.now();
        return exerciseCheckinMapper.selectTodayRecommendedExercises(userId, date);
    }

    /**
     *     @Override
     *     public void addNewToday(ExerciseRecommend exercise) {
     *         List<Map> list = new ArrayList<>();
     *         Map temp = new HashMap<>();
     *         temp.put("userId", BaseContext.getCurrentId());
     *         temp.put("now", LocalDateTime.now());
     *         temp.put("exerciseId", exercise.getExerciseId());
     *         temp.put("exerciseName", exercise.getExerciseName());
     *         temp.put("duration", exercise.getDuration());
     *         temp.put("caloriesBurned", exercise.getDuration() * exercise.getCaloriesBurnRate() / 10);//每10分钟
     *         list.add(temp);
     *         exerciseCheckinMapper.insertBatch(list);
     *     }
     * @param exercise
     */


    @Override
    public void addNewToday(ExerciseRecommend exercise) {
        Long userId = BaseContext.getCurrentId();
        LocalDate today = LocalDate.now();

        // 查询当天未checkin的同类运动
        List<ExerciseCheckin> todayUncheckins = exerciseCheckinMapper.selectTodayUncheckinByUser(userId, today);

        // 查找是否有重复的 exerciseId
        ExerciseCheckin matched = null;
        for (ExerciseCheckin record : todayUncheckins) {
            if (record.getExerciseId().equals(exercise.getExerciseId())) {
                matched = record;
                break;
            }
        }

        if (matched != null) {
            // 如果有重复记录，合并时长和卡路里，更新
            int newDuration = matched.getDuration() + exercise.getDuration();
            int newCalories = matched.getCaloriesBurned() + exercise.getDuration() * exercise.getCaloriesBurnRate() / 10;

            matched.setDuration(newDuration);
            matched.setCaloriesBurned(newCalories);
            matched.setCreateTime(LocalDateTime.now());

            exerciseCheckinMapper.updateById(matched);
        } else {
            // 否则插入新记录
            ExerciseCheckin newRecord = new ExerciseCheckin();
            newRecord.setUserId(userId.intValue());
            newRecord.setExerciseId(exercise.getExerciseId());
            newRecord.setExerciseName(exercise.getExerciseName());
            newRecord.setDuration(exercise.getDuration());
            newRecord.setCaloriesBurned(exercise.getDuration() * exercise.getCaloriesBurnRate() / 10);
            newRecord.setCreateTime(LocalDateTime.now());

            exerciseCheckinMapper.insert(newRecord);
        }
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
