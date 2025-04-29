package com.example.utils;

import java.util.List;
import java.util.stream.Collectors;

public class ListUtils {

    /**
     * 将字符串列表用顿号连接
     * @param list 原始列表（可包含null和空值）
     * @param skipEmpty 是否跳过空值
     * @param defaultValue null的替代值
     * @return 连接后的字符串
     * 使用示例：
     * List<String> test = Arrays.asList("A", null, "", "B");
     * String r1 = joinWithDun(test, true, "未知");
     * // 输出：A、未知、B（跳过了空字符串）
     * String r2 = joinWithDun(test, false, "空值");
     * // 输出：A、空值、、B（保留所有元素）
     */
    public String joinWithDun(List<String> list, boolean skipEmpty, String defaultValue) {
        if (list == null || list.isEmpty()) return "";

        return list.stream()
                .map(s -> s == null ? defaultValue : s)
                .filter(s -> !skipEmpty || !s.trim().isEmpty())
                .collect(Collectors.joining("、"));
    }
}
