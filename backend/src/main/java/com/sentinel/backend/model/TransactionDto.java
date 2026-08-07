package com.sentinel.backend.model;

import lombok.Data;

@Data
public class TransactionDto {
    private String customerId;
    private Double amount;
    private Double merchantRisk;
    private Integer nightTime;
    private Integer velocity;
    private Integer geoJump;
    private Integer newDevice;
    private Integer vpnUsed;
    private Double spendDeviation;
    private Integer failedAttempts;
}
