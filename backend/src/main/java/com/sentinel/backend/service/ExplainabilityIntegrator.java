package com.sentinel.backend.service;

import com.sentinel.backend.model.TransactionDto;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Slf4j
public class ExplainabilityIntegrator {

    private final RestTemplate restTemplate;

    @Value("${app.ai-service.url}")
    private String aiServiceUrl;

    public AiPredictionResult getPredictionAndExplainability(TransactionDto tx) {
        try {
            String url = aiServiceUrl + "/predict";
            
            // Map the camelCase DTO to the PascalCase/snake_case expected by AI Service
            Map<String, Object> aiPayload = new java.util.HashMap<>();
            aiPayload.put("customer_id", tx.getCustomerId());
            aiPayload.put("Amount", tx.getAmount());
            aiPayload.put("MerchantCategoryRisk", tx.getMerchantRisk());
            aiPayload.put("NightTime", tx.getNightTime());
            aiPayload.put("Velocity", tx.getVelocity());
            aiPayload.put("GeographicJump", tx.getGeoJump());
            aiPayload.put("NewDevice", tx.getNewDevice());
            aiPayload.put("VPNUsed", tx.getVpnUsed());
            aiPayload.put("SpendDeviation", tx.getSpendDeviation());
            aiPayload.put("FailedAttempts", tx.getFailedAttempts());

            ResponseEntity<AiPredictionResult> response = restTemplate.postForEntity(url, aiPayload, AiPredictionResult.class);
            return response.getBody();
        } catch (Exception e) {
            log.error("Failed to fetch prediction from AI service", e);
            // Fallback object to not crash the stream
            AiPredictionResult fallback = new AiPredictionResult();
            fallback.setMl_probability(0.0);
            fallback.setNarrative("AI Service unavailable.");
            return fallback;
        }
    }

    @Data
    public static class AiPredictionResult {
        private Double ml_probability;
        private List<Map<String, Object>> explanations;
        private String narrative;
        private String model_name;
        // ignoring the python-side composite scoring, as we do it in Java now.
    }
}
