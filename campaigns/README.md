# Campaigns App - Phishing Simulation System

## Overview

The campaigns app provides phishing simulation and tracking functionality for PhishGuard. It allows organizations to send simulated phishing emails to employees and track who clicks on malicious links, helping identify security awareness gaps.

## Core Features

- **Unique Link Tracking**: Each employee receives a unique UUID-based tracking link
- **Click Recording**: Automatically records timestamps when employees click links
- **Educational Landing Page**: Shows phishing awareness content when links are clicked
- **Campaign Management**: Create, send, and monitor phishing simulation campaigns
- **Analytics Dashboard**: View click-through rates and per-employee results
- **Email Templates**: Reusable phishing email templates with difficulty levels

## Quick Start

### 1. Create Email Template (Admin Panel)

```
Name: Password Reset Simulation
Subject: Your password will expire today
Body: <html>...<a href="{{tracking_link}}">Reset Now</a>...</html>
Difficulty: Medium
```

### 2. Create Campaign

```python
# Via web interface at /campaigns/create/
Campaign Name: Q4 2025 Security Training
Template: Password Reset Simulation
Employees: [Select employees from checkboxes]
```

### 3. Send Campaign

```python
# Via web interface at /campaigns/<id>/send/
# System automatically:
# - Generates unique UUID for each employee
# - Replaces {{tracking_link}} with tracking URL
# - Sends emails via SMTP
# - Records sent_at timestamp
```

### 4. Track Results

```python
# View at /campaigns/<id>/
# Shows:
# - Total targets
# - Emails sent
# - Links clicked
# - Click rate percentage
# - Per-employee status and timestamps
```

## Models

### EmailTemplate
Reusable phishing email templates.

**Fields:**
- `name`: Template identifier
- `subject_line`: Email subject
- `body_html`: HTML content (must include `{{tracking_link}}`)
- `sender_name`: Display name for sender
- `sender_email`: From address
- `difficulty_level`: EASY, MEDIUM, HARD
- `phishing_indicators`: Description of red flags

### Campaign
Represents a phishing simulation campaign.

**Fields:**
- `organization`: ForeignKey to Organization
- `name`: Campaign identifier
- `description`: Optional details
- `status`: DRAFT, SCHEDULED, ACTIVE, COMPLETED
- `email_template`: ForeignKey to EmailTemplate
- `created_by`: ForeignKey to User
- `created_at`, `updated_at`: Timestamps

### CampaignTarget
Tracks individual employee interaction with campaign.

**Fields:**
- `campaign`: ForeignKey to Campaign
- `employee`: ForeignKey to Employee
- `unique_tracking_token`: UUID4 (unique, indexed)
- `sent_at`: When email was sent
- `email_opened_at`: When email was opened (future)
- `link_clicked_at`: When link was clicked
- `reported_at`: When phishing was reported (future)
- `status`: PENDING, SENT, OPENED, CLICKED, REPORTED

**Constraints:**
- `unique_together`: [campaign, employee]
- Each employee can only be targeted once per campaign

## Views

### campaign_list
**URL:** `/campaigns/`  
**Permission:** Login required  
**Purpose:** List all campaigns for user's organization

### create_campaign
**URL:** `/campaigns/create/`  
**Permission:** Login required, must have organization  
**Purpose:** Create new campaign and select targets

### campaign_detail
**URL:** `/campaigns/<id>/`  
**Permission:** Login required, ownership verified  
**Purpose:** View statistics and target list

### send_campaign
**URL:** `/campaigns/<id>/send/`  
**Permission:** Login required, ownership verified  
**Purpose:** Send phishing emails to all pending targets

### track_click
**URL:** `/campaigns/track/<uuid>/`  
**Permission:** None (embedded in emails)  
**Purpose:** Record click and show educational page

## URL Patterns

```python
urlpatterns = [
    path('', campaign_list, name='campaign_list'),
    path('create/', create_campaign, name='create_campaign'),
    path('<int:campaign_id>/', campaign_detail, name='campaign_detail'),
    path('<int:campaign_id>/send/', send_campaign, name='send_campaign'),
    path('track/<uuid:token>/', track_click, name='track_click'),
]
```

## Tracking Flow

1. **Campaign Creation**
   - User creates campaign
   - Selects email template
   - Chooses target employees
   - System creates CampaignTarget for each employee
   - Each gets unique UUID4 token

2. **Email Sending**
   - User clicks "Send Campaign"
   - For each target:
     - Build tracking URL with unique token
     - Replace `{{tracking_link}}` in template
     - Send email via SMTP
     - Update status to SENT
     - Record sent_at timestamp

3. **Click Tracking**
   - Employee clicks link in email
   - Request hits `/campaigns/track/<token>/`
   - System looks up CampaignTarget by token
   - Records link_clicked_at timestamp
   - Updates status to CLICKED
   - Shows educational landing page

4. **Analytics**
   - User views campaign details
   - System calculates:
     - Total targets
     - Sent count
     - Clicked count
     - Click rate percentage
   - Shows per-employee table with statuses

## Security

### Unique Tokens (UUID4)
- 128-bit random identifier
- Cryptographically secure
- ~5.3 × 10^36 possible values
- Impossible to guess or brute-force

### Ownership Verification
```python
if campaign.organization.owner != request.user:
    return error
```
Users can only access their organization's campaigns.

### CSRF Protection
- All management views: CSRF required
- Exception: `track_click` (@csrf_exempt)
  - Email links can't include CSRF tokens
  - Token itself provides security
  - Read-only operation

### Database Constraints
- `unique_together`: Prevents duplicate targets
- Token uniqueness enforced at DB level

## Email Configuration

### Development (Gmail)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
```

**Setup:**
1. Enable 2FA on Google account
2. Generate App Password
3. Set environment variables

**Limits:** ~100 emails/day

### Production Alternatives
- **Amazon SES**: $0.10 per 1,000 emails
- **SendGrid**: 100/day free, $19.95/month for 50k
- **Postmark**: $15/month for 10,000 emails
- **Mailgun**: 5,000/month free

## Templates

### Email Template Requirements
Must include `{{tracking_link}}` placeholder:

```html
<a href="{{tracking_link}}" style="...">
    Click Here to Reset Password
</a>
```

### Available Django Templates
- `campaign_list.html`: Dashboard
- `create_campaign.html`: Creation form
- `campaign_detail.html`: Statistics and results
- `send_campaign.html`: Confirmation page
- `phishing_revealed.html`: Educational landing page

## Admin Interface

Registered models in Django admin:
- EmailTemplate: Create/edit templates
- Campaign: View all campaigns
- CampaignTarget: View tracking records

Access at: `/admin/campaigns/`

## Testing

### Manual Test
1. Add yourself as an employee
2. Create campaign targeting yourself
3. Send campaign
4. Check your email
5. Click the link
6. Verify click was recorded

### Create Sample Templates
```bash
python3 manage.py shell < create_sample_templates.py
```

Creates 3 templates:
- Urgent Password Reset (Medium)
- Package Delivery Notification (Easy)
- CEO Email Request (Hard)

## Future Enhancements

- [ ] Email open tracking (tracking pixels)
- [ ] Scheduled sending (Celery integration)
- [ ] Employee reporting functionality
- [ ] Advanced analytics (time-to-click, trends)
- [ ] Template library expansion
- [ ] Export reports (PDF/CSV)
- [ ] Subscription-based feature gating
- [ ] A/B testing different templates
- [ ] Department-level analytics
- [ ] Custom landing pages per template

## Dependencies

- Django 6.0
- Python 3.x
- SMTP email server access
- orgs app (for Organization and Employee models)

## Files

```
campaigns/
├── __init__.py
├── admin.py           # Admin configuration
├── apps.py
├── models.py          # EmailTemplate, Campaign, CampaignTarget
├── tests.py
├── urls.py            # URL routing
├── views.py           # All views
├── migrations/
│   ├── __init__.py
│   └── 0001_initial.py
└── templates/
    └── campaigns/
        ├── campaign_list.html
        ├── create_campaign.html
        ├── campaign_detail.html
        ├── send_campaign.html
        └── phishing_revealed.html
```

## Support Documentation

- `IMPLEMENTATION_SUMMARY.md`: Full implementation details
- `CAMPAIGN_SETUP.md`: Setup and configuration guide
- `QUICK_TEST.md`: Quick testing instructions
- `ARCHITECTURE.md`: System architecture and flow diagrams

## License

Part of PhishGuard project.
