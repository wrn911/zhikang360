package com.example.DAO;
import lombok.Data;
import java.util.List;
@Data
public class IllnessInfoDAO {

    private Allergy allergy;


    private List<String> chronicDiseases;


    private String healthIssues;

    @Data
    public static class Allergy {
        private String type;

        private List<String> details;
    }
}
