package com.example.service;

import com.example.DAO.CheckinCountDTO;
import com.example.common.enums.BadgeStandardTypeEnum;
import com.example.context.BaseContext;
import com.example.entity.*;
import com.example.DAO.FoodCheckinAddRequest;
import com.example.DAO.FoodCheckinStatsDAO;
import java.time.format.DateTimeFormatter;

import com.example.mapper.BadgeStandardMapper;
import com.example.mapper.FoodMapper;
import com.example.mapper.FoodCheckinMapper;
import java.time.YearMonth;

import com.example.mapper.UserBasicInfoMapper;
import com.example.utils.MedalConstants;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

@Service
public class FoodCheckinService {

    @Resource
    private FoodCheckinMapper foodCheckinMapper;

    @Autowired
    private FoodMapper foodMapper;
    @Autowired
    private UserBasicInfoMapper userBasicInfoMapper;
    @Autowired
    private BadgeStandardMapper badgeStandardMapper;


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
        int[] foodAdd = MedalConstants.FOOD_ADD_DAYS;
        int[] foodContinue = MedalConstants.FOOD_CONTINUE_DAYS;
        int[] foodCal = MedalConstants.FOOD_CALORIE_THRESHOLD;
        Long userId = BaseContext.getCurrentId();
        UserCheckInfo userCheckInfo = userBasicInfoMapper.selectCheckInfoById(userId);
        CheckinCountDTO checkinCountDTO = foodCheckinMapper.selectCheckinCounts(userId);
        Integer medalDay;

        // 饮食累计打卡勋章检查
        if(checkinCountDTO.getTodayCount() == 0){
            Integer addDay = userCheckInfo.getFoodAddDay();
            userCheckInfo.setFoodAddDay(addDay+1);
            medalDay = 0;
            for(int i = 0 ; i < foodAdd.length ; i++){
                if(foodAdd[i] == addDay+1){
                    medalDay = foodAdd[i];
                }else if(foodAdd[i] > addDay+1){
                    break;
                }else{
                    continue;
                }
            }
            if(medalDay > 0){
               Integer badgeId = badgeStandardMapper.selectIdByTypeAndDays(BadgeStandardTypeEnum.饮食打卡天数.name(),medalDay);
               MyBadge myBadge = new MyBadge(userId, badgeId, true);
               badgeStandardMapper.insertPersonBadge(myBadge);
                blockChainLink(badgeId);
            }
        }

        //饮食连续打卡勋章检查
        if(checkinCountDTO.getYesterdayCount() > 0 && checkinCountDTO.getTodayCount() == 0){
            Integer continueDay = userCheckInfo.getFoodContinueDay();
            userCheckInfo.setFoodContinueDay(continueDay+1);
            medalDay = 0;
            for(int i = 0 ; i < foodContinue.length ; i++){
                if(foodContinue[i] == continueDay+1){
                    medalDay = foodContinue[i];
                }else if(foodContinue[i] > continueDay+1){
                    break;
                }else{
                    continue;
                }
            }
            if(medalDay > 0){
                Integer badgeId = badgeStandardMapper.selectIdByTypeAndDays(BadgeStandardTypeEnum.饮食连续打卡天数.name(), medalDay);
                MyBadge myBadge = new MyBadge(userId, badgeId, true);
                badgeStandardMapper.insertPersonBadge(myBadge);
                blockChainLink(badgeId);
            }
        }

        if(checkinCountDTO.getYesterdayCount() == 0 && checkinCountDTO.getTodayCount() == 0){
            userCheckInfo.setFoodContinueDay(1);
        }

        // 总卡路里摄入勋章检查
        Double cal = userCheckInfo.getAddFoodCal();
        Double calNew = cal + addCal;
        userCheckInfo.setAddFoodCal(calNew);
        medalDay = 0;
        for(int i = 0 ; i < foodCal.length ; i++){
            if(foodCal[i] > cal && foodCal[i] <= calNew){
                medalDay = foodCal[i];
            }else if(foodCal[i] > calNew){
                break;
            }else{
                continue;
            }
        }
        if(medalDay > 0){
            Integer badgeId = badgeStandardMapper.selectIdByTypeAndDays(BadgeStandardTypeEnum.饮食记录摄入.name(), medalDay);
            MyBadge myBadge = new MyBadge(userId, badgeId, true);
            badgeStandardMapper.insertPersonBadge(myBadge);
            blockChainLink(badgeId);
        }

        userBasicInfoMapper.updateCheckInfo(userCheckInfo);

    }

    @Transactional
    public void add(FoodCheckinAddRequest foodCheckinAddRequest) {
        Long userId = BaseContext.getCurrentId();
        Integer foodId = foodCheckinAddRequest.getFoodId();
        String mealType = foodCheckinAddRequest.getMealType().getChineseName();
        Food food = foodMapper.selectById(foodCheckinAddRequest.getFoodId());
        Double b = (double) foodCheckinAddRequest.getGrams() / 100 ;
        Double addCal = Math.round(food.getCalories() * b * 10) / 10.0;
        this.checkMedal(addCal);
        LocalDate today = LocalDate.now();
        FoodCheckin foodCheckin = foodCheckinMapper.selectByUserIdAndFoodId(userId ,foodId ,mealType,today);
        if(foodCheckin == null){
            foodCheckin = new FoodCheckin();
            foodCheckin.setUserId(userId);
            foodCheckin.setFoodId(foodId);
            foodCheckin.setFoodName(foodCheckinAddRequest.getFoodName());
            foodCheckin.setCheckinType(mealType);
            foodCheckin.setGramAte(foodCheckinAddRequest.getGrams());
            foodCheckin.setCaloriesAte(addCal);
            foodCheckin.setCarbohydratesAte(Math.round(food.getCarbohydrates() * b * 10) / 10.0);
            foodCheckin.setFatAte(Math.round(food.getFat() * b * 10) / 10.0);
            foodCheckin.setProteinAte(Math.round(food.getProtein() * b * 10) / 10.0);
            foodCheckin.setFiberAte(Math.round(food.getFiber() * b * 10) / 10.0);
            foodCheckin.setCreateTime(LocalDateTime.now());
            foodCheckinMapper.insert(foodCheckin);
        }else{
            foodCheckin.setGramAte(foodCheckinAddRequest.getGrams() + foodCheckin.getGramAte());
            addCal = Math.round(food.getCalories() * b * 10) / 10.0;
            foodCheckin.setCaloriesAte(addCal + foodCheckin.getCaloriesAte());
            foodCheckin.setCarbohydratesAte(Math.round(food.getCarbohydrates() * b * 10) / 10.0 + foodCheckin.getCarbohydratesAte());
            foodCheckin.setFatAte(Math.round(food.getFat() * b * 10) / 10.0 + foodCheckin.getFatAte());
            foodCheckin.setProteinAte(Math.round(food.getProtein() * b * 10) / 10.0 + foodCheckin.getProteinAte());
            foodCheckin.setFiberAte(Math.round(food.getFiber() * b * 10) / 10.0 + foodCheckin.getFiberAte());
            foodCheckin.setCreateTime(LocalDateTime.now());
            foodCheckinMapper.updateById(foodCheckin);
        }

    }

    public void deleteById(Integer checkinId) {
        foodCheckinMapper.deleteById(checkinId);
    }

    public void updateById(FoodCheckin foodCheckin) {
        foodCheckinMapper.updateById(foodCheckin);
    }

    public FoodCheckin selectById(Integer checkinId) {
        return foodCheckinMapper.selectById(checkinId);
    }

    public Map<String, ArrayList<Food>> simpleSelect() {
        List<Food> foods = foodMapper.selectAll(new Food());
        Map<String, ArrayList<Food>> foodMap = new HashMap<>();
        //格式：食物类型：【相关食物】
        for (Food food : foods) {
            if(food.getCategory().equals("")){
                food.setCategory("暂无");
            }
            if (!foodMap.containsKey(food.getCategory())) {
                foodMap.put(food.getCategory(), new ArrayList<>());
            }
            foodMap.get(food.getCategory()).add(food);
        }
        return foodMap;
    }


    public Map<String, ArrayList<FoodCheckin>> simpleSelectCheckin() {
        Long userId = BaseContext.getCurrentId();
        LocalDate today = LocalDate.now();
        String date = today.toString();
        List<FoodCheckin> foodCheckins = foodCheckinMapper.selectHistory(userId , date);
        Map<String, ArrayList<FoodCheckin>> foodCheckinMap = new HashMap<>();
        //格式：食物类型：【相关食物】
        for (FoodCheckin foodCheckin : foodCheckins) {
            if (!foodCheckinMap.containsKey(foodCheckin.getCheckinType())) {
                foodCheckinMap.put(foodCheckin.getCheckinType(), new ArrayList<>());
            }
            foodCheckinMap.get(foodCheckin.getCheckinType()).add(foodCheckin);
        }
        return foodCheckinMap;
    }

    public FoodCheckinStatsDAO selectCheckinDaysAndCalories() {
        FoodCheckinStatsDAO foodCheckinStatsDAO = new FoodCheckinStatsDAO();
        Long userId = BaseContext.getCurrentId();
        LocalDate today = LocalDate.now();
        String s = today.toString();
        String month = LocalDate.now().format(DateTimeFormatter.ofPattern("yyyy-MM"));
        Integer checkinDays = foodCheckinMapper.countCheckinDays(month, userId);
        Double finalCalories = foodCheckinMapper.sumCalories(month, userId);
        Integer daysInMonth = YearMonth.now().lengthOfMonth();
        foodCheckinStatsDAO.setSelectedDate(s);
        foodCheckinStatsDAO.setCheckinDays(checkinDays);
        foodCheckinStatsDAO.setFinalCalories(finalCalories);
        foodCheckinStatsDAO.setTotalDays(daysInMonth);
        return foodCheckinStatsDAO;
    }

    public Map<String, ArrayList<FoodCheckin>> selectHistory(String date) {
        Long userId = BaseContext.getCurrentId();
        List<FoodCheckin> foodCheckins = foodCheckinMapper.selectHistory(userId,date);
        Map<String, ArrayList<FoodCheckin>> resultMap = new HashMap<>();
        for (FoodCheckin foodCheckin : foodCheckins) {
            if (!resultMap.containsKey(foodCheckin.getCheckinType())){
                resultMap.put(foodCheckin.getCheckinType(), new ArrayList<>());
            }
            resultMap.get(foodCheckin.getCheckinType()).add(foodCheckin);
        }
        return resultMap;
    }
}
