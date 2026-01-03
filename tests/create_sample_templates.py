#!/usr/bin/env python3
"""
Sample script to create test email templates via Django shell.
Run with: python3 manage.py shell < create_sample_templates.py
"""

from campaigns.models import EmailTemplate

# Sample Template 1: Password Reset (Medium Difficulty)
EmailTemplate.objects.get_or_create(
    name="Urgent Password Reset",
    defaults={
        'subject_line': "⚠️ Your password will expire today",
        'sender_name': "IT Security Team",
        'sender_email': "it-security@company.com",
        'difficulty_level': "MEDIUM",
        'phishing_indicators': """
- Creates urgency ("expire today")
- Threatens account suspension
- Generic greeting
- Suspicious sender email
- Urgent call-to-action button
        """,
        'body_html': """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto;">
    <div style="background-color: #f44336; color: white; padding: 20px; text-align: center;">
        <h2 style="margin: 0;">⚠️ Password Expiration Notice</h2>
    </div>
    
    <div style="padding: 30px; background-color: #ffffff;">
        <p>Dear Employee,</p>
        
        <p>Your company password will expire <strong>today at 5:00 PM</strong>. 
        To avoid account suspension, please reset your password immediately.</p>
        
        <p>Click the button below to reset your password:</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{{tracking_link}}" 
               style="background-color: #1976d2; 
                      color: white; 
                      padding: 15px 30px; 
                      text-decoration: none; 
                      border-radius: 5px;
                      display: inline-block;
                      font-weight: bold;">
                Reset Password Now
            </a>
        </div>
        
        <p style="color: #d32f2f; font-weight: bold;">
            ⏰ Time Remaining: Less than 8 hours
        </p>
        
        <p style="color: #666; font-size: 12px; border-top: 1px solid #ddd; padding-top: 20px; margin-top: 30px;">
            If you don't reset your password within 24 hours, your account will be locked 
            and require administrator assistance to unlock.
        </p>
        
        <p>Thank you,<br>
        IT Security Team</p>
    </div>
</body>
</html>
        """
    }
)

# Sample Template 2: Package Delivery (Easy Difficulty)
EmailTemplate.objects.get_or_create(
    name="Package Delivery Notification",
    defaults={
        'subject_line': "Package Delivery Attempted - Action Required",
        'sender_name': "UPS Delivery",
        'sender_email': "delivery@ups-notify.com",
        'difficulty_level': "EASY",
        'phishing_indicators': """
- Unexpected package notification
- Suspicious domain (ups-notify.com instead of ups.com)
- Requests immediate action
- Generic greeting
- Creates urgency
        """,
        'body_html': """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto;">
    <div style="background-color: #351c15; color: #ffb500; padding: 20px;">
        <h2 style="margin: 0;">📦 UPS Delivery Notification</h2>
    </div>
    
    <div style="padding: 30px; background-color: #ffffff;">
        <p>Hello,</p>
        
        <p>We attempted to deliver your package today, but no one was available to receive it.</p>
        
        <p><strong>Tracking Number:</strong> 1Z999AA10123456784</p>
        
        <p>To reschedule your delivery or arrange for pickup, please confirm your delivery address:</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{{tracking_link}}" 
               style="background-color: #ffb500; 
                      color: #351c15; 
                      padding: 15px 30px; 
                      text-decoration: none; 
                      border-radius: 5px;
                      display: inline-block;
                      font-weight: bold;">
                Confirm Delivery Address
            </a>
        </div>
        
        <p style="color: #d32f2f;">
            <strong>Important:</strong> If you don't respond within 48 hours, 
            your package will be returned to sender.
        </p>
        
        <p style="color: #666; font-size: 12px; margin-top: 30px;">
            UPS Tracking Department<br>
            Phone: 1-800-PICK-UPS
        </p>
    </div>
</body>
</html>
        """
    }
)

# Sample Template 3: CEO Email (Hard Difficulty)
EmailTemplate.objects.get_or_create(
    name="Urgent Request from CEO",
    defaults={
        'subject_line': "Re: Urgent Wire Transfer Needed",
        'sender_name': "Sarah Johnson, CEO",
        'sender_email': "s.johnson@company-ceo.net",
        'difficulty_level': "HARD",
        'phishing_indicators': """
- Impersonates executive
- Requests urgent financial action
- Domain slightly different from real company domain
- Requests confidentiality
- Creates pressure with urgency
- Uses "Re:" to appear like continuing conversation
        """,
        'body_html': """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto; padding: 20px;">
    <p>Hi there,</p>
    
    <p>I'm currently in meetings with potential investors and need your immediate assistance 
    with a time-sensitive matter.</p>
    
    <p>We need to process an urgent wire transfer for a business acquisition that closes today. 
    I'm unable to access our normal systems from here, so I need you to handle this directly.</p>
    
    <p>Please click here to access the secure payment portal with the wire details:</p>
    
    <div style="margin: 20px 0;">
        <a href="{{tracking_link}}" 
           style="color: #1976d2; text-decoration: underline;">
            Access Secure Payment Portal
        </a>
    </div>
    
    <p><strong>Please keep this confidential</strong> as we haven't announced the acquisition yet. 
    The deal needs to close by end of business today.</p>
    
    <p>Let me know once it's done. I'll be in meetings all afternoon but check your email when I can.</p>
    
    <p>Thanks for your quick action on this.</p>
    
    <p>Best regards,<br>
    Sarah Johnson<br>
    <span style="color: #666; font-size: 12px;">
    Chief Executive Officer<br>
    Company Name<br>
    Mobile: +1 (555) 123-4567
    </span></p>
</body>
</html>
        """
    }
)

print("✅ Successfully created 3 sample email templates!")
print("\nTemplates created:")
print("1. Urgent Password Reset (Medium)")
print("2. Package Delivery Notification (Easy)")
print("3. Urgent Request from CEO (Hard)")
print("\nYou can now create campaigns using these templates.")
