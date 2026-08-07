package com.sentinel.backend.controller;

import com.sentinel.backend.model.FraudCase;
import com.sentinel.backend.repository.FraudCaseRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequestMapping("/api/cases")
@RequiredArgsConstructor
public class CaseManagementController {

    private final FraudCaseRepository fraudCaseRepository;

    @GetMapping
    @PreAuthorize("hasAnyRole('ANALYST', 'ADMIN')")
    public ResponseEntity<List<FraudCase>> getAllCases() {
        return ResponseEntity.ok(fraudCaseRepository.findAll());
    }

    @PostMapping("/{id}/status")
    @PreAuthorize("hasAnyRole('ANALYST', 'ADMIN')")
    public ResponseEntity<FraudCase> updateCaseStatus(@PathVariable Long id, @RequestParam String status) {
        return fraudCaseRepository.findById(id).map(c -> {
            c.setStatus(status.toUpperCase());
            c.setUpdatedAt(LocalDateTime.now());
            // Here you would also log an audit event
            return ResponseEntity.ok(fraudCaseRepository.save(c));
        }).orElse(ResponseEntity.notFound().build());
    }
}
