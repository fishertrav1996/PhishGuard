# PhishGuard Campaign System - Setup Guide

## Overview
The phishing simulation tracking system is now implemented! Here's how to use it.

## Setup Steps

### 1. Configure Gmail SMTP (for testing)

Set up environment variables for email sending:

```bash
export EMAIL_HOST_USER='your-email@gmail.com'
export EMAIL_HOST_PASSWORD='your-app-password'
```

**To get a Gmail App Password:**
1. Enable 2-Factor Authentication on your Google account
2. Go to: Google Account → Security → App passwords
3. Generate a new app password for "Mail"
4. Use that 16-character password (not your regular Gmail password)

### 2. Create Email Templates

You need at least one email template before creating campaigns. Do this through the Django admin:

1. Start the server: `python3 manage.py runserver`
2. Go to: http://localhost:8000/admin/
3. Navigate to: Campaigns → Email templates → Add
4. Fill in the template details (see sample below)

**Important:** Include `{{tracking_link}}` in the HTML body where you want the clickable link!

### Sample Email Template:

**Name:** Password Reset Phishing  
**Subject Line:** Urgent: Your password will expire today  
**Sender Name:** IT Security Team  
**Sender Email:** it-security@company.com  
**Difficulty:** Medium

**Body HTML:**
```html
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6;">
    <h2 style="color: #d32f2f;">⚠️ Password Expiration Notice</h2>
    
    <p>Dear Employee,</p>
    
    <p>Your company password will expire <strong>today at 5:00 PM</strong>. 
    To avoid account suspension, please reset your password immediately.</p>
    
    <p>Click the button below to reset your password:</p>
    
    <p style="margin: 30px 0;">
        <a href="{{tracking_link}}" 
           style="background-color: #1976d2; 
                  color: white; 
                  padding: 12px 24px; 
                  text-decoration: none; 
                  border-radius: 4px;
                  display: inline-block;">
            Reset Password Now
        </a>
    </p>
    
    <p style="color: #666; font-size: 12px;">
        If you don't reset your password within 24 hours, 
        your account will be locked and require administrator assistance to unlock.
    </p>
    
    <p>Thank you,<br>
    IT Security Team</p>
</body>
</html>
```

**Phishing Indicators:**
- Creates urgency with "today at 5:00 PM"
- Threatens account suspension
- Generic greeting ("Dear Employee")
- Suspicious sender email address
- Urgent call-to-action button

## How to Use the System

### 1. Create a Campaign

1. Navigate to: http://localhost:8000/campaigns/
2. Click "Create Campaign"
3. Fill in:
   - Campaign name (e.g., "Q4 2025 Security Training")
   - Description (optional)
   - Select an email template
   - Select target employees (checkboxes)
4. Click "Create Campaign"

### 2. Send the Campaign

1. From the campaign detail page, click "Send Campaign"
2. Review the details
3. Click "Send X Emails"
4. Emails will be sent immediately with unique tracking links

### 3. Monitor Results

- View campaign details to see:
  - Total targets
  - Emails sent
  - Links clicked
  - Click rate percentage
- The table shows per-employee status and click timestamps

### 4. When Employees Click

When an employee clicks the tracking link:
1. Their click is recorded with timestamp
2. Status changes to "CLICKED"
3. They see an educational page explaining:
   - This was a simulation
   - What phishing is
   - How to spot phishing emails
   - What to do if they receive real phishing

## Database Models

### EmailTemplate
- Reusable phishing email templates
- Contains subject, body (HTML), sender info
- Difficulty levels: Easy, Medium, Hard
- Use `{{tracking_link}}` placeholder for the tracking URL

### Campaign
- Represents a single phishing simulation campaign
- Belongs to an Organization
- Has status: DRAFT → ACTIVE → COMPLETED
- References an EmailTemplate

### CampaignTarget
- Junction table between Campaign and Employee
- Stores unique tracking token (UUID)
- Tracks: sent_at, link_clicked_at, reported_at
- Status: PENDING → SENT → CLICKED

## URL Structure

- `/campaigns/` - List all campaigns
- `/campaigns/create/` - Create new campaign
- `/campaigns/<id>/` - View campaign details
- `/campaigns/<id>/send/` - Send campaign emails
- `/campaigns/track/<uuid>/` - Track link clicks (embedded in emails)

## Security Features

1. **Unique Tokens:** Each employee gets a UUID4 tracking token
2. **Ownership Verification:** Users can only manage their organization's campaigns
3. **CSRF Protection:** Maintained except for tracking endpoint (emails can't include CSRF tokens)
4. **Login Required:** All management views require authentication

## Gmail Limits

- **Free Gmail:** ~100 emails/day
- For production, switch to:
  - Amazon SES (cheapest)
  - SendGrid (good deliverability)
  - Postmark (best for transactional emails)

## Next Steps

1. Create email templates in admin
2. Create a test campaign with yourself as target
3. Send the campaign
4. Click the link to see the educational page
5. Check the campaign statistics

## Tips

- Test with small groups first
- Create templates with varying difficulty levels
- Monitor click rates to assess employee awareness
- Use results to plan additional training
- Consider scheduling campaigns quarterly

## Production Deployment

Before going to production:
1. Change `DEBUG = False` in settings.py
2. Set up proper email backend (not Gmail)
3. Use environment variables for all secrets
4. Set `ALLOWED_HOSTS` properly
5. Use HTTPS for tracking links
6. Consider implementing email open tracking (tracking pixels)
7. Add scheduled sending with Celery
