package com.sentinel.backend.service;

import org.springframework.stereotype.Service;

@Service
public class CompositeRiskEngine {

    // Default weights, could be pulled from DB in future
    private static final double W_ML = 0.5;
    private static final double W_RULE = 0.3;
    private static final double W_BEHAVIOR = 0.2;

    public CompositeRiskResult calculateScore(double mlProb, double ruleScore, double behaviorScore) {
        double mlScore = mlProb * 100.0;
        
        double finalScore = (mlScore * W_ML) + (ruleScore * W_RULE) + (behaviorScore * W_BEHAVIOR);
        finalScore = Math.min(Math.max(finalScore, 0.0), 100.0);
        
        return new CompositeRiskResult(finalScore, getRiskBand(finalScore));
    }

    private String getRiskBand(double score) {
        if (score <= 30) return "Safe";
        if (score <= 60) return "Low Risk";
        if (score <= 80) return "Suspicious";
        return "Fraud";
    }

    public record CompositeRiskResult(double compositeScore, String riskBand) {}
}
