package com.example.mapper;

import com.example.entity.Feedback;
import org.apache.ibatis.annotations.Mapper;
import java.time.LocalDate;
import java.util.List;

@Mapper
public interface FeedbackMapper {
    void insert(Feedback feedback);
    Feedback selectByUserIdAndDate(Long userId, LocalDate date);
    List<Feedback> selectAllByUserId(Long userId);
    void deleteById(int id);
    void update(Feedback feedback);
}

