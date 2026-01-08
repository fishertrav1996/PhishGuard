# PhishGuard Logging & Audit Trail Roadmap

## Overview
Production-quality logging infrastructure for debugging, security monitoring, compliance auditing, and performance optimization.

---

## Phase 1: Campaign Operations Logging (High Priority)

### Campaign Lifecycle Events
```python
# Campaign Creation
- LOG: Campaign created
- Data: campaign_uuid, org_uuid, creator_user_id, template_id, target_count, timestamp
- Level: INFO

# Email Sending
- LOG: Campaign email sent (per target)
- Data: campaign_uuid, target_email, sent_status (success/failure), error_message, timestamp
- Level: INFO (success), ERROR (failure)

# Delivery Tracking
- LOG: Email delivery status updates
- Data: campaign_uuid, target_email, delivery_status, bounce_reason, timestamp
- Level: WARNING (bounces)
```

### User Interaction Tracking
```python
# Link Clicks
- LOG: Phishing link clicked
- Data: campaign_uuid, employee_id, target_uuid, ip_address, user_agent, timestamp
- Level: INFO
- Security: Track suspicious patterns (multiple IPs, automated tools)

# Remediation Events
- LOG: Remediation assigned/completed
- Data: target_uuid, employee_id, assigned_at, completed_at, completion_time_minutes
- Level: INFO
```

---

## Phase 2: Authentication & Security Logging (High Priority)

### Authentication Events
```python
# Login Attempts
- LOG: User login attempt
- Data: username, ip_address, success/failure, failure_reason, timestamp
- Level: INFO (success), WARNING (failure)

# Failed Login Rate Limiting
- LOG: Multiple failed login attempts
- Data: username/ip_address, attempt_count, lockout_triggered, timestamp
- Level: WARNING (threshold), ERROR (lockout)

# Logout
- LOG: User logout
- Data: username, session_duration, timestamp
- Level: INFO
```

### Email Verification
```python
# Verification Attempts
- LOG: Email verification attempt
- Data: user_id, token_valid, verification_success, ip_address, timestamp
- Level: INFO (success), WARNING (invalid token)

# Rate Limiting
- LOG: Verification email resend requested
- Data: user_id, resend_count, rate_limit_hit, timestamp
- Level: WARNING (rate limit)
```

---

## Phase 3: Subscription & Billing Logging (Medium Priority)

### Subscription Changes
```python
# Tier Changes
- LOG: Subscription tier changed
- Data: org_uuid, old_tier, new_tier, changed_by_user_id, timestamp
- Level: INFO

# Trial Expiration
- LOG: Free trial expired
- Data: org_uuid, campaigns_used, trial_start_date, expiration_date
- Level: INFO

# Limit Enforcement
- LOG: Campaign limit reached
- Data: org_uuid, current_tier, limit_reached, attempt_count, timestamp
- Level: WARNING
```

### Payment Events (Stripe)
```python
# Payment Success
- LOG: Payment processed successfully
- Data: org_uuid, amount, stripe_payment_id, timestamp
- Level: INFO

# Payment Failure
- LOG: Payment failed
- Data: org_uuid, amount, failure_reason, retry_count, timestamp
- Level: ERROR

# Webhook Processing
- LOG: Stripe webhook received
- Data: event_type, event_id, processing_status, timestamp
- Level: INFO
```

---

## Phase 4: Compliance & Reporting Logging (Medium Priority)

### Report Generation
```python
# Compliance Report Created
- LOG: Compliance report generated
- Data: report_uuid, org_uuid, report_type, frameworks, period_start, period_end, timestamp
- Level: INFO

# Report Downloaded
- LOG: Compliance report downloaded
- Data: report_uuid, downloaded_by_user_id, ip_address, timestamp
- Level: INFO

# Report Deleted
- LOG: Compliance report deleted
- Data: report_uuid, deleted_by_user_id, reason, timestamp
- Level: WARNING
```

---

## Phase 5: Performance & System Monitoring (Low Priority)

### Email Sending Performance
```python
# Batch Email Metrics
- LOG: Bulk email campaign completed
- Data: campaign_uuid, total_emails, success_count, failure_count, duration_seconds
- Level: INFO

# Slow Email Operations
- LOG: Email sending took longer than expected
- Data: campaign_uuid, duration_seconds, threshold_seconds
- Level: WARNING
```

### Database Performance
```python
# Slow Queries
- LOG: Database query exceeded performance threshold
- Data: query_type, duration_ms, model, threshold_ms
- Level: WARNING
```

---

## Implementation Guidelines

### Log Levels
- **DEBUG**: Development debugging only, never in production
- **INFO**: Normal operations (campaign created, email sent, user logged in)
- **WARNING**: Concerning but recoverable (failed login, rate limit hit, bounced email)
- **ERROR**: Failed operations requiring attention (payment failed, email sending failed)
- **CRITICAL**: System-level failures (database connection lost, AWS SES quota exceeded)

### Data Privacy & Security
1. **Never log passwords** or sensitive authentication tokens
2. **Hash/mask PII** in logs (email addresses, names)
3. **Sanitize user inputs** before logging to prevent log injection
4. **Redact sensitive fields** in Stripe webhook logs (card numbers, CVV)
5. **Implement log retention policies** (90 days for operational, 7 years for compliance)

### Log Storage Strategy
```
Development:
- Console output + local file (phishguard.log)

Production:
- Centralized logging (CloudWatch, Datadog, Sentry)
- Structured JSON format for parsing
- Log aggregation and alerting
- Separate logs by severity
```

### Security Monitoring Patterns
```python
# Suspicious Activity Detection
1. Multiple failed logins from same IP (brute force)
2. Rapid campaign creation (abuse detection)
3. Unusual download patterns (data exfiltration)
4. Verification tokens used multiple times (token reuse attack)
5. High bounce rates (invalid email lists)
```

---

## Integration Points

### Current Logging Configuration
Location: `PhishGuard/settings.py`

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
        'file': {'class': 'logging.FileHandler', 'filename': 'logs/phishguard.log'},
    },
    'loggers': {
        'accounts': {'handlers': ['console', 'file'], 'level': 'INFO'},
        'campaigns': {'handlers': ['console', 'file'], 'level': 'INFO'},
    },
}
```

### Adding Logging to Views
```python
import logging
logger = logging.getLogger(__name__)

# Example usage
logger.info(f"Campaign created: {campaign.uuid} by user {request.user.id}")
logger.warning(f"Campaign limit reached for org {org.uuid}")
logger.error(f"Failed to send email to {target.email}: {error}")
```

---

## Priority Implementation Order

1. **Phase 1** - Campaign logging (immediate need for debugging)
2. **Phase 2** - Authentication logging (security requirement)
3. **Phase 3** - Subscription logging (before Stripe integration)
4. **Phase 4** - Compliance logging (regulatory requirement)
5. **Phase 5** - Performance monitoring (optimization)

---

## Success Metrics

- [ ] All critical operations logged
- [ ] Security incidents detectable within logs
- [ ] Compliance audit trail complete
- [ ] Performance bottlenecks identifiable
- [ ] Zero sensitive data leakage in logs
- [ ] Log retention policy enforced
- [ ] Alerting configured for critical errors
