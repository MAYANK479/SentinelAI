package com.sentinel.backend.service;

import com.sentinel.backend.model.TransactionDto;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;

@Service
@EnableScheduling
@RequiredArgsConstructor
@Slf4j
public class TransactionSimulatorService {

    private final SimpMessagingTemplate messagingTemplate;
    private final RuleEvaluator ruleEvaluator;
    private final CompositeRiskEngine riskEngine;
    private final ExplainabilityIntegrator aiIntegrator;
    private final Random random = new Random();

    // Simulates a transaction every 5 seconds
    @Scheduled(fixedRate = 5000)
    public void simulateAndProcessTransaction() {
        TransactionDto tx = generateRandomTransaction();
        
        // 1. Evaluate Heuristic Rules
        RuleEvaluator.RuleEvaluationResult ruleResult = ruleEvaluator.evaluate(tx);
        
        // 2. Fetch AI Prediction
        ExplainabilityIntegrator.AiPredictionResult aiResult = aiIntegrator.getPredictionAndExplainability(tx);
        
        // 3. (Mocked Behavior Score for now - Phase 2 focuses on wiring)
        double behaviorScore = 50.0;
        
        // 4. Calculate Final Composite Risk
        CompositeRiskEngine.CompositeRiskResult finalRisk = riskEngine.calculateScore(
                aiResult.getMl_probability() != null ? aiResult.getMl_probability() : 0.0,
                ruleResult.score(),
                behaviorScore
        );
        
        // Build payload
        Map<String, Object> payload = new HashMap<>();
        payload.put("transaction", tx);
        payload.put("rulesTriggered", ruleResult.triggeredRules());
        payload.put("aiProbability", aiResult.getMl_probability());
        payload.put("narrative", aiResult.getNarrative());
        payload.put("compositeScore", finalRisk.compositeScore());
        payload.put("riskBand", finalRisk.riskBand());
        
        // Publish to WebSocket
        messagingTemplate.convertAndSend("/topic/live-transactions", (Object) payload);
        
        if (finalRisk.compositeScore() > 80.0) {
            messagingTemplate.convertAndSend("/topic/alerts", (Object) payload);
            // In a full implementation, we'd also save to DB and create a FraudCase here.
        }
    }
    
    private TransactionDto generateRandomTransaction() {
        TransactionDto tx = new TransactionDto();
        tx.setCustomerId("CUST_" + String.format("%04d", random.nextInt(1000)));
        tx.setAmount(10 + (1000 - 10) * random.nextDouble());
        tx.setMerchantRisk(random.nextDouble());
        tx.setNightTime(random.nextDouble() > 0.8 ? 1 : 0);
        tx.setVelocity(1 + random.nextInt(5));
        tx.setGeoJump(random.nextDouble() > 0.95 ? 1 : 0);
        tx.setNewDevice(random.nextDouble() > 0.9 ? 1 : 0);
        tx.setVpnUsed(random.nextDouble() > 0.9 ? 1 : 0);
        tx.setSpendDeviation(random.nextDouble() * 3);
        tx.setFailedAttempts(random.nextDouble() > 0.9 ? 1 : 0);
        return tx;
    }
}
