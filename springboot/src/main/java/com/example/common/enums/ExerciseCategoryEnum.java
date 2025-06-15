package com.example.common.enums;

import java.util.Random;

public enum ExerciseCategoryEnum {
    有氧运动,力量训练,球类运动,游泳,武术格斗;

    public static ExerciseCategoryEnum getRandomCategory() {
        ExerciseCategoryEnum[] values = ExerciseCategoryEnum.values();
        Random random = new Random();
        int index = 2 + random.nextInt(3); // 只随机 2, 3, 4
        return values[index];
    }
}
