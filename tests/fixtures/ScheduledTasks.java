package com.example.scheduler;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class ReportScheduler {

    // cron-based schedule
    @Scheduled(cron = "0 0 8 * * MON-FRI")
    public void generateDailyReport() {
        // business logic
    }

    // fixed-rate schedule
    @Scheduled(fixedRate = 60000)
    public void syncInventory() {
        // business logic
    }

    // fixed-delay schedule
    @Scheduled(fixedDelay = 30000)
    public void cleanupExpiredSessions() {
        // business logic
    }

    // unscheduled helper — must NOT produce a TRIGGERS edge
    public void helperMethod() {}
}
