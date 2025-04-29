package com.example.DAO;

import lombok.Data;

import java.util.List;
@Data
public class SportInfoDAO {
    private String preferences;
    private String weaknesses;
    private String willingness;
    private String experience;
    private String intensity;
    private List<String> freeTime;
}
