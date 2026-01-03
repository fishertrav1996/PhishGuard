# PhishGuard Revenue Features - Implementation Roadmap

This document outlines the implementation plan for transforming PhishGuard from MVP to a revenue-ready SaaS platform.

## 🎯 Strategic Goals

1. **Make it mandatory** - Compliance-driven value proposition
2. **Enable self-service** - Onboard without hand-holding
3. **Justify paid tier** - Clear value differentiation
4. **Support hybrid sales** - Admin-assisted flow when needed

---

## 📊 Current State Assessment

### ✅ Completed Foundation
- ✅ Multi-tenant organizations with UUID tracking
- ✅ Phishing campaign creation and delivery
- ✅ Per-employee unique tracking tokens
- ✅ Click tracking with timestamps
- ✅ Basic analytics dashboard
- ✅ Email template system
- ✅ CSV employee bulk upload
- ✅ Role-based membership system (OWNER, ADMIN, MEMBER, BILLING)
- ✅ Organization and campaign management
- ✅ Educational landing page on click

### ⚠️ Missing Revenue Features
- ❌ Compliance-ready reporting (PDF/CSV exports)
- ❌ Remediation tracking and workflows
- ❌ Subscription enforcement and paywalls
- ❌ Self-service onboarding flow
- ❌ Healthcare-specific templates (content)
- ❌ Admin impersonation/management tools

---

## 🗺️ Implementation Roadmap

### **Phase 1: Foundation for Revenue (Week 1)**
**Goal:** Enable compliance evidence and differentiate paid tier

#### Feature 1.1: Remediation Workflows ⭐ P0
**Why First:** Foundation for compliance reports, relatively self-contained

**What to Build:**
- Add fields to CampaignTarget model:
  - `remediation_assigned_at` (timestamp)
  - `remediation_completed_at` (timestamp)
- Update phishing_revealed.html landing page:
  - Add educational content
  - Add acknowledgment checkbox: "I understand the risks"
  - Add submit button
- Create remediation completion view/endpoint
- Update campaign analytics to show remediation stats
- Update campaign detail page with remediation column

**Database Changes:**
```python
# CampaignTarget model additions
remediation_assigned_at = models.DateTimeField(null=True, blank=True)
remediation_completed_at = models.DateTimeField(null=True, blank=True)
```

**Views/URLs:**
- `POST /campaigns/track/<token>/complete/` - Mark remediation complete
- Update `track_click` to auto-assign remediation

**Success Criteria:**
- ✓ Clicking phishing link auto-assigns remediation
- ✓ User can complete acknowledgment
- ✓ Timestamps recorded accurately
- ✓ Campaign detail shows remediation status

**Estimated Effort:** 1.5-2 days

---

#### Feature 1.2: Compliance-Ready Reporting ⭐ P0
**Why Second:** Builds on remediation data, highest revenue impact

**What to Build:**

**A. Report Models:**
```python
class ComplianceReport(models.Model):
    organization = FK
    campaign = FK (nullable - for org-level reports)
    report_type = choices: CAMPAIGN, ORGANIZATION, QUARTERLY
    generated_by = FK User
    generated_at = timestamp
    file_path = FileField or CharField (S3 path)
    format = choices: PDF, CSV
```

**B. Report Generation:**
- PDF reports using `weasyprint`
- CSV exports using Django CSV writer
- Report data aggregation:
  - Organization name, campaign details, date ranges
  - Sent/clicked/reported counts and percentages
  - Remediation completion stats
  - Per-employee breakdown (anonymized option available)
  - **Compliance statements for:**
    - **HIPAA** (Health Insurance Portability and Accountability Act)
    - **HITECH** (Health Information Technology for Economic and Clinical Health Act)
    - **HITRUST CSF** (Health Information Trust Alliance Common Security Framework)
  - Evidence of due diligence for cyber insurance
  - Training completion documentation

**C. Compliance Statement Templates:**
Include standardized statements in reports:

```
HIPAA Security Rule Compliance:
"This organization conducts routine security awareness training and 
phishing simulations as required under the HIPAA Security Rule 
(45 CFR § 164.308(a)(5)). This report documents employee training 
activities and security testing performed during [DATE RANGE]."

HITECH Act Breach Prevention:
"In accordance with the HITECH Act breach notification requirements, 
this organization implements proactive security measures including 
regular phishing simulations to reduce the risk of unauthorized 
PHI disclosure. This report provides evidence of ongoing security 
awareness efforts."

HITRUST CSF Control Evidence:
"This report provides documented evidence for HITRUST CSF controls:
- 01.h Security Awareness Training
- 09.g Information Security Event Management
- 02.i User Training
Demonstrating measurable security awareness metrics and incident response preparedness."

Cyber Insurance Documentation:
"This report provides evidence of proactive cybersecurity measures 
for insurance compliance, demonstrating:
- Regular employee security testing
- Documented click-through rates
- Remediation and training completion
- Ongoing risk assessment activities"
```

**D. Report Content Requirements:**
- **Executive Summary:** High-level metrics and trends
- **Campaign Details:** Template used, difficulty level, sending dates
- **Employee Performance:** Anonymized or detailed breakdown
- **Risk Assessment:** Identify high-risk departments/roles
- **Remediation Status:** Training completion rates
- **Recommendations:** Next steps to improve security posture
- **Compliance Attestation:** Signed statement of training completion
- **Appendix:** Detailed click timeline, employee roster (optional)

**C. Views & URLs:**
- `GET /campaigns/<uuid>/report/pdf/` - Generate campaign PDF
- `GET /campaigns/<uuid>/report/csv/` - Export campaign CSV
- `GET /orgs/<uuid>/reports/` - List all reports
- `GET /orgs/<uuid>/report/generate/` - Generate org-level report
- `GET /reports/<uuid>/download/` - Download existing report (with auth check)

**D. File Storage Structure:**
```
MEDIA_ROOT/compliance_reports/
├── {org_uuid}/
│   ├── 2026/
│   │   ├── 01/
│   │   │   ├── {report_uuid}.pdf
│   │   │   └── {report_uuid}.csv
│   │   └── 02/
│   └── 2025/
└── .gitignore  # Exclude from version control
```

**E. Templates:**
- `reports/compliance_report.html` - PDF template (WeasyPrint format)
- `campaigns/report_list.html` - Report listing page
- Include CSS for professional PDF styling
- Healthcare organization branding support

**E. Permissions:**
- Check `org_membership.can_export_reports()`
- Restrict to OWNER and ADMIN roles only
- Audit log all report generation events
- Watermark reports with generated date and user info

**F. Compliance Features:**
- Digital signature option for attestation
- Report retention policy (recommend 7 years for HIPAA)
- Audit trail of who generated/accessed reports
- Option to anonymize employee names (for executive reports)
- Export both detailed and summary versions

**Success Criteria:**
- ✓ PDF report generated with org branding
- ✓ CSV export with all campaign data
- ✓ Reports include compliance statement
- ✓ Reports stored/retrievable
- ✓ Only authorized users can generate

**Estimated Effort:** 3-4 days

**Dependencies:**
- Remediation workflow (for complete data)
- Add to requirements.txt: `weasyprint`, `pillow`
- Configure MEDIA_ROOT and MEDIA_URL in settings
- Create media directory structure
- Add report download permissions

---

#### Feature 1.3: Healthcare-Specific Templates 📋 P2
**Why Third:** Quick win, content-focused, differentiator

**What to Build:**
- Create 6-8 email templates via Django admin
- Template scenarios:
  1. EHR Password Reset (Medium difficulty)
  2. Lab Result Notification (Easy)
  3. Pharmacy Order Delay (Easy)
  4. IT Ticket Closure (Medium)
  5. Insurance Verification Required (Medium)
  6. Patient Portal Security Update (Hard)
  7. Medical Records Access Request (Hard)
  8. HIPAA Training Reminder (Easy)

**Database Changes:**
```python
# EmailTemplate model additions
scenario_type = models.CharField(choices=SCENARIO_TYPES, null=True)
target_audience = models.CharField(choices=AUDIENCE_TYPES, null=True)
compliance_notes = models.TextField(blank=True)

SCENARIO_TYPES = [
    ('EHR', 'EHR/EMR System'),
    ('LAB', 'Laboratory'),
    ('PHARMACY', 'Pharmacy'),
    ('IT_SUPPORT', 'IT Support'),
    ('INSURANCE', 'Insurance/Billing'),
    ('PATIENT_PORTAL', 'Patient Portal'),
    ('RECORDS', 'Medical Records'),
    ('TRAINING', 'Training/Compliance'),
]
```

**Content Requirements:**
- Realistic healthcare context
- Appropriate urgency levels
- Documented red flags for each template
- Difficulty ratings

**Success Criteria:**
- ✓ 8 templates created with healthcare themes
- ✓ Templates categorized by scenario type
- ✓ Red flags documented in each template
- ✓ Templates available in campaign creation

**Estimated Effort:** 1 day (mostly content writing)

---

### **Phase 2: Revenue Enablement (Week 2)**

#### Feature 2.1: Subscription Enforcement & Paywall ⭐ P0
**Why Now:** Enables revenue, requires no prior features

**What to Build:**

**A. Feature Gates:**
Create utility module: `orgs/subscription.py`
```python
def check_campaign_limit(organization):
    """Free: 1 active, Premium: unlimited"""
    
def check_employee_limit(organization):
    """Free: 25, Premium: unlimited"""
    
def can_export_reports(organization):
    """Free: No, Premium: Yes"""
    
def can_track_remediation(organization):
    """Free: No, Premium: Yes"""
```

**B. View Enforcement:**
- Update `create_campaign` view - check limits
- Update `add_employee`/`upload_csv` views - check limits
- Update report generation views - check subscription
- Update campaign detail view - gate remediation display

**C. UI Elements:**
- Upgrade prompts when limits reached
- Feature comparison modal
- "Upgrade to Premium" buttons
- Limit indicators (e.g., "2/25 employees used")

**D. Templates:**
- `orgs/upgrade_prompt.html` - Upgrade modal/page
- `orgs/subscription_manage.html` - Subscription management

**E. Database:**
- Organization already has subscription fields ✓
- Add field: `subscription_started_at`, `subscription_expires_at`

**Success Criteria:**
- ✓ Free tier limited to 1 campaign, 25 employees
- ✓ Premium gets unlimited campaigns/employees
- ✓ Export and remediation gated to Premium
- ✓ Graceful upgrade prompts shown
- ✓ Admin can manually toggle subscription

**Estimated Effort:** 2-3 days

**Integration Points:**
- Stripe Checkout integration for subscriptions
- Webhook endpoints for subscription events
- Subscription management admin tools
- Add fields to Organization model:
  - `stripe_customer_id`
  - `stripe_subscription_id`
  - `subscription_started_at`
  - `subscription_expires_at`
  - `payment_method_on_file` (boolean)

**Stripe Setup:**
- Create Stripe account and get API keys
- Set up webhook endpoint: `/webhooks/stripe/`
- Handle events: `customer.subscription.created`, `customer.subscription.deleted`, `invoice.payment_failed`
- Test mode first, then production keys

---

#### Feature 2.2: Self-Service Onboarding ⭐ P1
**Why Now:** Growth driver, requires subscription system

**What to Build:**

**A. Combined Signup Flow:**
- Merge account creation + org creation
- Single multi-step form or wizard
- Auto-create OWNER membership

**B. Onboarding Checklist Model:**
```python
class OnboardingProgress(models.Model):
    organization = OneToOne
    completed_signup = Boolean
    added_employees = Boolean
    created_first_campaign = Boolean
    sent_first_campaign = Boolean
    completed_at = timestamp
```

**C. Onboarding Dashboard:**
- Checklist UI showing progress
- Quick links to next steps
- Celebration on completion

**D. Templates & Views:**
- `accounts/signup_wizard.html` - Multi-step signup
- `core/onboarding_dashboard.html` - Progress tracker
- Update home page to show onboarding for new users

**E. Default Content:**
- Pre-populate 2-3 sample templates on org creation
- Welcome email (optional)

**Success Criteria:**
- ✓ New user can signup + create org in one flow
- ✓ Onboarding checklist visible after signup
- ✓ Progress tracked and displayed
- ✓ Can complete first campaign within 10 minutes
- ✓ Sample templates available immediately

**Estimated Effort:** 2-3 days

**Dependencies:**
- Healthcare templates (for defaults)
- Subscription system (for tier selection)

---

### **Phase 3: Admin & Scale (Week 3+)**

#### Feature 3.1: Hybrid Admin-Controlled Mode 🔧 P3
**Why Last:** Sales support, not critical for self-service launch

**What to Build:**

**A. Superadmin Dashboard:**
- List all organizations
- Search and filter
- Quick actions (impersonate, manage subscription)

**B. Impersonation:**
- Create membership with special flag: `is_support_access=True`
- Audit log for impersonation events
- Banner when in impersonation mode

**C. Organization Management Flags:**
```python
# Organization model additions
account_status = models.CharField(choices=STATUS_CHOICES)
is_trial = models.BooleanField(default=False)
trial_expires_at = models.DateTimeField(null=True)
account_manager = models.ForeignKey(User, null=True)
notes = models.TextField(blank=True)  # Internal notes

STATUS_CHOICES = [
    ('ACTIVE', 'Active'),
    ('TRIAL', 'Trial'),
    ('SUSPENDED', 'Suspended'),
    ('CANCELLED', 'Cancelled'),
]
```

**D. Admin Actions:**
- Manually create campaigns on behalf of orgs
- Generate reports for customers
- Adjust subscription/limits
- View detailed analytics

**Success Criteria:**
- ✓ Support staff can impersonate org admins
- ✓ All impersonation events logged
- ✓ Trial accounts managed with expiration
- ✓ Account status tracked
- ✓ Internal notes for account management

**Estimated Effort:** 2-3 days

---

#### Feature 3.2: Audit Logging (Stretch)
**What to Build:**
```python
class AuditLog(models.Model):
    organization = FK
    user = FK
    action = CharField  # 'campaign_created', 'report_exported', etc.
    timestamp = DateTime
    ip_address = GenericIPAddress
    details = JSONField
```

**Events to Log:**
- Campaign created/sent
- Reports generated
- Employees added/removed
- Subscription changes
- Impersonation sessions

**Estimated Effort:** 1-2 days

---

## 📦 Implementation Order Summary

### Week 1: Core Revenue Features
```
Day 1-2:   Remediation Workflows
Day 3-5:   Compliance Reporting (PDF + CSV)
Day 6-7:   Healthcare Templates (content)
```

### Week 2: Revenue Enablement
```
Day 1-3:   Subscription Enforcement & Paywalls
Day 4-6:   Self-Service Onboarding
Day 7:     Testing & Polish
```

### Week 3: Admin & Polish
```
Day 1-3:   Admin-Controlled Mode
Day 4-5:   Audit Logging (optional)
Day 6-7:   Bug fixes, documentation, launch prep
```

---

## 🧰 Technical Requirements

### New Python Packages
```txt
weasyprint>=60.0      # PDF generation (HTML to PDF, secure and reliable)
pillow>=10.0          # Image handling for PDFs
stripe>=7.0           # Payment processing
django-storages>=1.14 # Future S3 integration (add when migrating from filesystem)
```

### PDF Generation - Decision: WeasyPrint
**Why WeasyPrint:**
- More secure (uses standard HTML/CSS, no code execution)
- Better for compliance (templates auditable as HTML)
- Easier to maintain (designers can edit)
- Better typography and layout control
- Industry standard for document generation

### File Storage - Decision: Filesystem (Phase 1)
**Implementation:**
- Store in `MEDIA_ROOT/compliance_reports/`
- Organized by: `{org_uuid}/{year}/{month}/{report_uuid}.pdf`
- Serve via Django's `FileResponse` with permission checks
- Add to `.gitignore`

**Future Migration to S3:**
- Use django-storages when scaling
- Minimal code changes (swap storage backend)
- Keep same permission checks

### Payment Integration - Decision: Stripe
**Implementation:**
- Stripe Checkout for subscriptions
- Webhook handling for subscription events
- Store `stripe_customer_id` and `stripe_subscription_id` on Organization model

### Database Migrations Needed
1. CampaignTarget: Add remediation fields
2. ComplianceReport: New model
3. EmailTemplate: Add scenario_type, target_audience
4. Organization: Add subscription dates, account_status
5. OnboardingProgress: New model
6. AuditLog: New model (optional)

### New Apps/Modules (Optional)
- `reporting/` - Dedicated app for compliance reports
- `subscriptions/` - Subscription management

---

## ✅ Success Metrics

### Phase 1 Complete When:
- [ ] Users can assign/complete remediation
- [ ] PDF & CSV reports generate successfully
- [ ] 8 healthcare templates available
- [ ] All features documented

### Phase 2 Complete When:
- [ ] Free tier limits enforced
- [ ] Premium features gated
- [ ] New users can onboard in <10 min
- [ ] Onboarding progress tracked

### Phase 3 Complete When:
- [ ] Support staff can manage accounts
- [ ] Impersonation works securely
- [ ] All admin actions logged
- [ ] Ready for beta customers

---

## 🚨 Risk Mitigation

### Technical Risks
- **PDF generation performance** - Test with large datasets, consider async
- **Email delivery at scale** - May need Mailgun/SendGrid eventually
- **Database growth** - Plan for partitioning/archiving old campaigns

### Product Risks
- **Pricing too low** - Start with conservative limits, adjust up
- **Feature creep** - Stick to roadmap, resist adding features
- **Compliance requirements** - Include statements for HIPAA, HITECH, HITRUST in reports
- **Data retention** - Implement 7-year retention policy for healthcare compliance
- **PHI concerns** - Employee performance data may be sensitive, offer anonymization

### Compliance & Security
- **HIPAA Business Associate Agreement** - May need BAA with larger customers
- **Data encryption** - Ensure reports stored encrypted at rest
- **Access logging** - Audit all report access for compliance
- **Export controls** - Limit who can export detailed employee data
- **Retention policy** - Auto-archive old reports per compliance requirements

---

## 🎓 Documentation Needed

As each feature is built, create in `/docs`:
- `REMEDIATION_IMPLEMENTATION.md`
- `REPORTING_IMPLEMENTATION.md`
- `SUBSCRIPTION_IMPLEMENTATION.md`
- `ONBOARDING_IMPLEMENTATION.md`

Update in `/tests`:
- `test_remediation.py`
- `test_reporting.py`
- `test_subscriptions.py`
- `test_onboarding.py`

---

## 🚀 Launch Checklist

Before going live with paid tiers:
- [ ] All Phase 1 & 2 features complete
- [ ] Stripe integration tested (test mode → production)
- [ ] Terms of Service + Privacy Policy written
- [ ] HIPAA Business Associate Agreement template prepared
- [ ] Pricing page created with feature comparison
- [ ] Email templates professional and healthcare-appropriate
- [ ] Compliance statements reviewed by legal counsel
- [ ] Error handling comprehensive
- [ ] Load testing completed
- [ ] Security audit passed (pen test recommended)
- [ ] HTTPS enforced in production
- [ ] Data encryption at rest enabled
- [ ] Backup strategy implemented
- [ ] Documentation complete
- [ ] Support process defined (HIPAA-compliant)
- [ ] Incident response plan documented

---

**Next Step:** Begin with Feature 1.1 (Remediation Workflows) - See detailed implementation plan above.

**Technical Decisions Made:**
1. ✅ **PDF Library:** WeasyPrint (secure, reliable, HTML-based)
2. ✅ **Payment:** Stripe integration (webhooks + checkout)
3. ✅ **Storage:** Filesystem now (S3 migration path ready)
4. ✅ **Compliance:** HIPAA, HITECH, HITRUST statements in all reports

**Compliance Framework Support:**
- ✅ HIPAA Security Rule (45 CFR § 164.308(a)(5))
- ✅ HITECH Act breach prevention documentation
- ✅ HITRUST CSF control evidence (01.h, 09.g, 02.i)
- ✅ Cyber insurance compliance documentation
- ✅ 7-year retention policy (HIPAA requirement)
- ✅ Audit logging for all report access

**Ready to start implementation!**
