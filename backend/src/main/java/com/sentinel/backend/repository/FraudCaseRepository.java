package com.sentinel.backend.repository;

import com.sentinel.backend.model.FraudCase;
import org.springframework.data.jpa.repository.JpaRepository;

public interface FraudCaseRepository extends JpaRepository<FraudCase, Long> {
}
