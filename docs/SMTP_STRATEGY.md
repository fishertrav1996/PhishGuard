# PhishGuard SMTP Strategy for Phishing Simulations

## 🚨 Critical Challenge: Phishing Simulation Email Delivery

Most standard email service providers (ESPs) have strict anti-phishing policies that will result in account suspension or domain blacklisting when sending simulated phishing emails. We need a specialized strategy.

---

## 📊 Provider Comparison

| Provider | Allows Phishing Sims? | Cost | Deliverability | Setup Complexity | Recommendation |
|----------|----------------------|------|----------------|------------------|----------------|
| **Amazon SES** | ✅ Yes (with approval) | Very Low ($0.10/1000) | High | Medium | ⭐ **Primary Choice** |
| **SendGrid** | ⚠️ Case-by-case | Medium | High | Medium | Backup Option |
| **Mailgun** | ⚠️ Restricted | Medium | High | Medium | Not Recommended |
| **Postmark** | ❌ No | High | Excellent | Low | Not Suitable |
| **KnowBe4 SMTP** | ✅ Yes (purpose-built) | High | Good | Low | Expensive Alternative |
| **Custom SMTP** | ✅ Yes (full control) | High | Variable | High | Enterprise Option |
| **Google Workspace** | ❌ No | Low | High | Low | ❌ Will Ban Account |

---

## ⭐ Recommended Strategy: Amazon SES

### Why Amazon SES?

1. **Explicitly Allows Security Testing**
   - AWS terms allow legitimate security awareness training
   - Proper use case documentation prevents account issues
   - Separate sending for transactional vs simulation emails

2. **Cost-Effective**
   - $0.10 per 1,000 emails
   - No monthly minimums
   - First 62,000 emails/month free (if hosted on EC2)

3. **Scalable & Reliable**
   - Industry-standard infrastructure
   - High deliverability rates
   - Built-in bounce/complaint handling

4. **Full Control**
   - Dedicated IP available
   - Custom return-path
   - Complete header control

### SES Setup Requirements

**1. Domain Configuration:**
```
Primary Domain: phishguard.io (for app/marketing emails)
Simulation Domain: simulations.phishguard.io (for phishing tests)
```

**2. DNS Records Required:**
```dns
# SPF Record
simulations.phishguard.io. IN TXT "v=spf1 include:amazonses.com ~all"

# DKIM Records (provided by AWS)
<selector>._domainkey.simulations.phishguard.io. IN CNAME <aws-value>

# DMARC Record
_dmarc.simulations.phishguard.io. IN TXT "v=DMARC1; p=none; rua=mailto:dmarc@phishguard.io"

# Custom Return-Path
bounces.simulations.phishguard.io. IN MX 10 feedback-smtp.us-east-1.amazonses.com
```

**3. Request Production Access:**

Submit to AWS with this explanation:
```
Use Case: Healthcare Security Awareness Training

We operate PhishGuard, a HIPAA-compliant phishing simulation platform 
for healthcare organizations. Our service sends authorized, controlled 
phishing simulations to employees of our customers as part of their 
security awareness training programs.

Key Points:
- All emails sent with explicit customer authorization
- Recipients are employees of organizations who purchased our service
- Clear unsubscribe mechanism in every email
- Educational landing page explains the simulation
- Compliance with CAN-SPAM Act
- Bounce/complaint monitoring implemented
- Separate domain for simulations (simulations.phishguard.io)

Expected Volume: 5,000-50,000 emails/month initially

This is legitimate security testing, not malicious phishing.
```

**4. Warm-Up Schedule:**
```
Week 1: 100 emails/day
Week 2: 500 emails/day
Week 3: 1,000 emails/day
Week 4: 5,000 emails/day
Week 5+: Full volume
```

Start with internal tests and engaged customers with good open rates.

---

## 🔧 Implementation Plan

### Phase 1: Development (Current - Using Gmail SMTP)
**Status:** Already configured ✅
- Gmail SMTP for initial testing
- Limited to ~500 emails/day
- Works for MVP and early testing
- **Switch to SES before customer launch**

### Phase 2: Pre-Launch (Week -2)
**Setup Amazon SES:**
1. Create AWS account (if not exists)
2. Request SES production access (allow 1-2 weeks)
3. Configure `simulations.phishguard.io` subdomain
4. Set up DNS records (SPF, DKIM, DMARC)
5. Verify domain in SES console
6. Configure bounce/complaint handling (SNS topics)
7. Set up CloudWatch monitoring

**Django Settings Update:**
```python
# settings.py

if DEBUG:
    # Development - Gmail
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.environ.get('GMAIL_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('GMAIL_PASSWORD')
    DEFAULT_FROM_EMAIL = 'PhishGuard <noreply@phishguard.io>'
else:
    # Production - Amazon SES
    EMAIL_BACKEND = 'django_ses.SESBackend'
    AWS_SES_REGION_NAME = 'us-east-1'
    AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
    DEFAULT_FROM_EMAIL = 'PhishGuard Simulations <noreply@simulations.phishguard.io>'
    
    # Use IAM role or credentials
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_SES_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SES_SECRET_ACCESS_KEY')
```

**Add to requirements.txt:**
```txt
django-ses>=3.5.0      # Amazon SES backend
boto3>=1.26.0          # AWS SDK
```

### Phase 3: Launch (Week 0)
1. Start warm-up process (100 emails/day)
2. Monitor bounce rates (<5%)
3. Monitor complaint rates (<0.1%)
4. Gradually increase volume per schedule
5. Watch for SES reputation dashboard warnings

### Phase 4: Production (Week 4+)
- Full production volume
- Automated bounce/complaint handling
- Regular reputation monitoring
- Separate notification emails to regular SMTP

---

## 📧 Email Separation Strategy

### Simulation Emails (SES - simulations.phishguard.io)
**Use For:**
- All phishing simulation campaigns
- Tracking links
- Simulated urgent requests
- "Dangerous" content

**Characteristics:**
- May have higher complaint rates
- Designed to look suspicious
- Link to tracking URLs
- No real account actions

### Transactional Emails (SES or SendGrid - phishguard.io)
**Use For:**
- User signup confirmations
- Password resets
- Subscription receipts
- System notifications
- Report generation alerts

**Characteristics:**
- High deliverability needed
- Should never be blocked
- Professional appearance
- Real account actions

**Implementation:**
```python
# campaigns/views.py
def send_phishing_email(target):
    send_mail(
        subject=template.subject_line,
        message='',
        html_message=email_body,
        from_email='Security Team <alert@simulations.phishguard.io>',
        recipient_list=[target.employee.email],
        fail_silently=False,
    )

# accounts/views.py  
def send_welcome_email(user):
    send_mail(
        subject='Welcome to PhishGuard',
        message='Welcome!',
        from_email='PhishGuard Team <hello@phishguard.io>',
        recipient_list=[user.email],
        fail_silently=False,
    )
```

---

## 🛡️ Deliverability Best Practices

### 1. Authentication (REQUIRED)
- ✅ SPF record configured
- ✅ DKIM signing enabled
- ✅ DMARC policy set (start with p=none)
- ✅ Reverse DNS (PTR) record if using dedicated IP

### 2. Content Best Practices
**Do:**
- Include clear unsubscribe mechanism
- Add physical mailing address (CAN-SPAM)
- Keep image-to-text ratio reasonable
- Use clean HTML
- Include alt text for images
- Test emails before campaigns

**Don't:**
- Use misleading subject lines (even in sims)
- Include malicious attachments
- Use URL shorteners excessively
- Send to purchased lists
- Ignore bounces

### 3. List Hygiene
- Remove hard bounces immediately
- Suppress complainers automatically
- Respect unsubscribe requests
- Only send to authorized recipients
- Verify employee emails before adding

### 4. Monitoring
**Key Metrics:**
```python
BOUNCE_RATE_THRESHOLD = 0.05  # 5% max
COMPLAINT_RATE_THRESHOLD = 0.001  # 0.1% max
```

- Monitor SES reputation dashboard daily
- Set up CloudWatch alarms
- Review bounce/complaint reports weekly
- Track deliverability by organization

---

## ⚠️ Risk Mitigation

### Potential Issues & Solutions

**Issue: SES Account Suspension**
- **Prevention:** Follow warm-up schedule, monitor metrics closely
- **Mitigation:** Have SendGrid account ready as backup
- **Recovery:** Document use case clearly, request review

**Issue: Domain Blacklisting**
- **Prevention:** Use separate simulation subdomain
- **Mitigation:** Main domain (phishguard.io) unaffected
- **Recovery:** Can switch to new simulation subdomain

**Issue: High Complaint Rates**
- **Prevention:** Clear opt-in, educational content
- **Mitigation:** Reduce campaign frequency
- **Recovery:** Pause campaigns, review content

**Issue: Customer Email Server Blocking**
- **Prevention:** Work with IT teams, whitelist requests
- **Mitigation:** Provide SPF/DKIM for whitelisting
- **Recovery:** Alternative delivery methods

---

## 💰 Cost Analysis

### Amazon SES Pricing
```
First 62,000 emails/month: FREE (if hosted on AWS EC2)
Additional emails: $0.10 per 1,000 emails

Example Costs:
- 10,000 emails/month: $0 (under free tier)
- 100,000 emails/month: $3.80/month
- 500,000 emails/month: $43.80/month
- 1,000,000 emails/month: $93.80/month

Dedicated IP: $24.95/month (not needed initially)
```

### SendGrid Pricing (Backup)
```
Free: 100 emails/day (3,000/month)
Essentials: $19.95/month (50,000 emails)
Pro: $89.95/month (100,000 emails)
Premier: Custom pricing (higher volume)
```

### Recommended Budget
```
Phase 1 (0-10k emails/month): $0 (Gmail → SES free tier)
Phase 2 (10-100k emails/month): $0-10/month (SES)
Phase 3 (100k-500k emails/month): $10-50/month (SES)
Scale (1M+ emails/month): $100-200/month (SES + dedicated IP)
```

---

## 🚀 Migration Checklist

### Pre-Launch
- [ ] Purchase `simulations.phishguard.io` domain
- [ ] Create AWS account for SES
- [ ] Request SES production access (2 weeks lead time)
- [ ] Configure DNS records (SPF, DKIM, DMARC)
- [ ] Verify domain in SES console
- [ ] Set up bounce/complaint handling (SNS → webhook)
- [ ] Install django-ses and boto3
- [ ] Update Django settings for SES
- [ ] Test with internal campaigns
- [ ] Create warm-up schedule

### Launch Week
- [ ] Start warm-up (100 emails/day)
- [ ] Monitor bounce/complaint rates
- [ ] Set up CloudWatch alarms
- [ ] Document any issues
- [ ] Increase volume per schedule

### Post-Launch
- [ ] Weekly reputation monitoring
- [ ] Monthly deliverability review
- [ ] Quarterly DNS record audit
- [ ] Customer feedback on deliverability

---

## 📚 Resources

### AWS SES Documentation
- [SES Developer Guide](https://docs.aws.amazon.com/ses/)
- [SES Best Practices](https://docs.aws.amazon.com/ses/latest/dg/best-practices.html)
- [Production Access Request](https://docs.aws.amazon.com/ses/latest/dg/request-production-access.html)

### Email Authentication
- [SPF Record Generator](https://www.spfwizard.net/)
- [DKIM Validator](https://dkimvalidator.com/)
- [DMARC Guide](https://dmarc.org/overview/)

### Testing Tools
- [Mail Tester](https://www.mail-tester.com/) - Email deliverability score
- [MXToolbox](https://mxtoolbox.com/) - DNS and blacklist checking
- [GlockApps](https://glockapps.com/) - Inbox placement testing

---

## ✅ Recommendation Summary

**Primary Strategy: Amazon SES + Dedicated Simulation Subdomain**

1. **Now (Development):** Continue using Gmail SMTP for testing
2. **Week -2 (Pre-Launch):** Request SES production access, configure DNS
3. **Week 0 (Launch):** Begin SES warm-up process
4. **Week 4+ (Production):** Full production volume on SES

**Backup Strategy: SendGrid Account (Ready but Unused)**
- Set up account but don't activate
- Request approval for security testing use case
- Keep credentials ready in case SES issues arise

**Cost:** $0-50/month for first year (under SES free tier + normal usage)

**Risk:** Low (with proper warm-up and monitoring)

**Compliance:** HIPAA-compliant (SES is HIPAA-eligible with BAA)

This strategy balances cost, reliability, and compliance while providing a clear path from development to production scale.
