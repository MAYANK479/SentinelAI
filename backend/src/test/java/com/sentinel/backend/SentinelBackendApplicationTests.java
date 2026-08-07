package com.sentinel.backend;

import com.sentinel.backend.model.TransactionDto;
import com.sentinel.backend.service.CompositeRiskEngine;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import org.springframework.test.context.ActiveProfiles;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
@ActiveProfiles("test")
class SentinelBackendApplicationTests {

    @Autowired
    private CompositeRiskEngine riskEngine;

    @Test
    void contextLoads() {
        // Verifies that the Spring application context loads successfully.
    }

    @Test
    void testCompositeRiskEngine() {
        // mlScore = 0.9, rulesScore = 50, behaviorScore = 40
        CompositeRiskEngine.CompositeRiskResult result = riskEngine.calculateScore(0.9, 50.0, 40.0);
        
        // 0.9 * 50 = 45
        // 50.0 * 30 / 100 = 15
        // 40.0 * 20 / 100 = 8
        // Total = 45 + 15 + 8 = 68
        assertThat(result.compositeScore()).isEqualTo(68.0);
        assertThat(result.riskBand()).isEqualTo("Suspicious");
    }

    @Test
    void testCompositeRiskEngine_HighRisk() {
        CompositeRiskEngine.CompositeRiskResult result = riskEngine.calculateScore(0.95, 100.0, 80.0);
        assertThat(result.riskBand()).isEqualTo("Fraud");
    }
}
