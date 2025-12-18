# PhishGuard - Quick Test Instructions

## Test the Complete Workflow

### Step 1: Set Gmail Credentials

```bash
# In your terminal:
export EMAIL_HOST_USER='fishertrav@gmail.com'
export EMAIL_HOST_PASSWORD='ktwduhlefybbeltu'
```

### Step 2: Create Sample Email Templates

```bash
python3 manage.py shell < create_sample_templates.py
```

### Step 3: Start the Development Server

```bash
python3 manage.py runserver
```

### Step 4: Login to Your Account

Navigate to: http://localhost:8000/accounts/login/

### Step 5: Create Test Employee (Add Yourself)

1. Go to your organization's employee list
2. Add yourself as an employee with your real email
3. This lets you test the phishing simulation safely

### Step 6: Create a Campaign

1. Navigate to: http://localhost:8000/campaigns/
2. Click "Create Campaign"
3. Fill in:
   - Name: "Test Campaign"
   - Select any template (e.g., "Urgent Password Reset")
   - Check your name in the employee list
4. Click "Create Campaign"

### Step 7: Send the Campaign

1. Click "Send Campaign" button
2. Review the details
3. Click "Send X Emails"
4. Wait a moment for the email to send

### Step 8: Check Your Email

1. Open your email inbox
2. Look for the phishing simulation email
3. **Don't worry** - this is your test!

### Step 9: Click the Link

1. Click the link in the email
2. You should see the educational landing page
3. It explains this was a simulation

### Step 10: View Results

1. Go back to: http://localhost:8000/campaigns/
2. Click on your test campaign
3. You should see:
   - ✅ 1 email sent
   - ✅ 1 link clicked
   - ✅ 100% click rate
   - ✅ Your name with a timestamp

## Verify Everything Works

✅ Campaign created successfully  
✅ Email sent to your inbox  
✅ Link clicked and recorded  
✅ Educational page displayed  
✅ Statistics updated correctly  

## Quick Admin Access

Access Django admin to manage templates:

```bash
# Create superuser if you haven't already
python3 manage.py createsuperuser
```

Then visit: http://localhost:8000/admin/

Under "Campaigns" section you can:
- View/edit EmailTemplates
- See all Campaigns
- Check CampaignTargets

## Troubleshooting

**No email received?**
- Check spam/junk folder
- Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are set
- Check Gmail sent folder to see if it sent
- Try sending a test email from Gmail web interface

**Template placeholder error?**
- Make sure template body contains `{{tracking_link}}`
- Check in admin: http://localhost:8000/admin/campaigns/emailtemplate/

**Can't create campaign?**
- Ensure you have at least one EmailTemplate
- Ensure you have at least one Employee in your organization
- Verify you're logged in as the organization owner

**Tracking link not working?**
- Check the URL in email - should be localhost:8000/campaigns/track/...
- Verify server is still running
- Check browser console for errors

## What to Look For

### In the Email
- Subject line from template
- Sender name from template
- Clickable link (may look suspicious on purpose!)
- Professional formatting

### On Click
- Educational page loads
- Your first name appears (if set in employee record)
- Campaign name shows
- Tips on spotting phishing

### In Dashboard
- Campaign status changes to "ACTIVE"
- Sent count = 1
- Clicked count = 1  
- Click rate = 100%
- Your row shows "CLICKED" status
- Timestamp shows when you clicked

## Next: Try Different Templates

Create campaigns with different difficulty levels:
- **Easy**: Package Delivery Notification (obvious fake domain)
- **Medium**: Urgent Password Reset (time pressure)
- **Hard**: CEO Email (authority + urgency + confidentiality)

See which templates have higher click rates!

## Production Notes

Before using with real employees:
1. Switch from Gmail to production email service
2. Test with small group first
3. Notify HR/Legal about security training
4. Set expectations (this is training, not punishment)
5. Use HTTPS domain for tracking links
6. Consider opt-out mechanism for privacy concerns

---

**Ready to start?** Run through steps 1-10 above!
