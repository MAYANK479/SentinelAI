package com.sentinel.backend.service;

import com.sentinel.backend.model.FraudRule;
import com.sentinel.backend.model.TransactionDto;
import com.sentinel.backend.repository.FraudRuleRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.expression.ExpressionParser;
import org.springframework.expression.spel.standard.SpelExpressionParser;
import org.springframework.expression.spel.support.StandardEvaluationContext;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class RuleEvaluator {

    private final FraudRuleRepository ruleRepository;
    private final ExpressionParser parser = new SpelExpressionParser();

    public static class EvaluationRoot {
        private final TransactionDto tx;
        public EvaluationRoot(TransactionDto tx) { this.tx = tx; }
        public TransactionDto getTx() { return tx; }
    }

    public RuleEvaluationResult evaluate(TransactionDto tx) {
        List<FraudRule> activeRules = ruleRepository.findByIsActiveTrue();
        StandardEvaluationContext context = new StandardEvaluationContext(new EvaluationRoot(tx));

        double totalScore = 0.0;
        List<String> triggeredRules = new ArrayList<>();

        for (FraudRule rule : activeRules) {
            try {
                Boolean result = parser.parseExpression(rule.getConditionExpression()).getValue(context, Boolean.class);
                if (Boolean.TRUE.equals(result)) {
                    totalScore += rule.getWeight();
                    triggeredRules.add(rule.getName());
                }
            } catch (Exception e) {
                log.error("Failed to evaluate rule: {}", rule.getName(), e);
            }
        }

        return new RuleEvaluationResult(Math.min(totalScore, 100.0), triggeredRules);
    }

    public record RuleEvaluationResult(double score, List<String> triggeredRules) {}
}
