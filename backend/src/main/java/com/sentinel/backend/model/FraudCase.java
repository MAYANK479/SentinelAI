package com.sentinel.backend.model;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Entity
@Table(name = "fraud_cases")
@Data
@NoArgsConstructor
public class FraudCase {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "transaction_id")
    private Long transactionId; // In a full relational mapping this would be @ManyToOne Transaction

    @ManyToOne
    @JoinColumn(name = "analyst_id")
    private User analyst;

    @Column(nullable = false)
    private String status = "OPEN"; // OPEN, ASSIGNED, UNDER_INVESTIGATION, RESOLVED, FALSE_POSITIVE

    @Column(name = "created_at", insertable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
}
