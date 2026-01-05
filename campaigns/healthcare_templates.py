#!/usr/bin/env python3
"""
Healthcare-specific phishing email templates for clinical and lab staff.
Run with: python manage.py shell < healthcare_templates.py
"""

from campaigns.models import EmailTemplate

# Template 1: EMR System Password Reset (Clinical Staff)
EmailTemplate.objects.get_or_create(
    name="Epic EMR Password Expiration",
    defaults={
        'subject_line': "Action Required: Your Epic Password Expires Today",
        'sender_name': "Epic IT Support",
        'sender_email': "epic-support@hospital-system.com",
        'difficulty_level': "MEDIUM",
        'scenario_type': "EMR_EHR_ACCESS",
        'target_audience': "CLINICAL_STAFF",
        'phishing_indicators': """
- Creates urgency with same-day expiration
- Suspicious sender domain (not official Epic domain)
- Generic greeting without personalization
- Requests immediate action
- External link for password reset
        """,
        'body_html': """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto;">
    <div style="background-color: #0066cc; color: white; padding: 20px;">
        <h2 style="margin: 0;">Epic EMR System Notice</h2>
    </div>
    
    <div style="padding: 30px; background-color: #ffffff;">
        <p>Dear Clinical Staff Member,</p>
        
        <p>Your Epic EMR system password is set to expire <strong>today at 11:59 PM</strong>. 
        If you don't reset it immediately, you will lose access to patient records and be unable 
        to complete documentation.</p>
        
        <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0;">
            <p style="margin: 0;"><strong>⚠️ Important:</strong> Failure to reset your password will 
            result in account suspension and require IT administrator approval to restore access.</p>
        </div>
        
        <p>Click the button below to reset your password now:</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{{tracking_link}}" 
               style="background-color: #0066cc; 
                      color: white; 
                      padding: 15px 40px; 
                      text-decoration: none; 
                      border-radius: 5px;
                      display: inline-block;
                      font-weight: bold;">
                Reset Epic Password
            </a>
        </div>
        
        <p style="color: #666; font-size: 12px; margin-top: 30px;">
            This is an automated message from the Epic IT Support Team.<br>
            For assistance, contact the Help Desk at ext. 5555
        </p>
    </div>
</body>
</html>
        """
    }
)

# Template 2: Lab Results Portal Access (Lab Staff)
EmailTemplate.objects.get_or_create(
    name="Laboratory Information System - Critical Update",
    defaults={
        'subject_line': "URGENT: LIS System Update Required - Action Needed",
        'sender_name': "Laboratory Systems",
        'sender_email': "lab-systems@hospital-notify.com",
        'difficulty_level': "MEDIUM",
        'scenario_type': "EMR_EHR_ACCESS",
        'target_audience': "LAB_STAFF",
        'phishing_indicators': """
- Creates false urgency with "URGENT" and "Critical"
- Suspicious sender domain
- Threatens loss of access to lab systems
- Requests immediate action
- External verification link
        """,
        'body_html': """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto;">
    <div style="background-color: #d32f2f; color: white; padding: 20px;">
        <h2 style="margin: 0;">🔬 Laboratory Information System Alert</h2>
    </div>
    
    <div style="padding: 30px; background-color: #ffffff;">
        <p>Dear Laboratory Staff,</p>
        
        <p>A critical security update has been deployed to the Laboratory Information System (LIS). 
        All lab personnel must verify their credentials within the next <strong>4 hours</strong> or 
        lose access to:</p>
        
        <ul style="color: #d32f2f;">
            <li>Patient lab results</li>
            <li>Specimen tracking system</li>
            <li>Quality control data</li>
            <li>Test ordering functionality</li>
        </ul>
        
        <div style="background-color: #ffebee; border-left: 4px solid #d32f2f; padding: 15px; margin: 20px 0;">
            <p style="margin: 0;"><strong>WARNING:</strong> This update affects all laboratory 
            departments including Chemistry, Hematology, Microbiology, and Blood Bank.</p>
        </div>
        
        <p>Click below to verify your LIS credentials and maintain system access:</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{{tracking_link}}" 
               style="background-color: #1976d2; 
                      color: white; 
                      padding: 15px 40px; 
                      text-decoration: none; 
                      border-radius: 5px;
                      display: inline-block;
                      font-weight: bold;">
                Verify LIS Credentials
            </a>
        </div>
        
        <p style="color: #666; font-size: 12px; margin-top: 30px;">
            Laboratory Systems Department<br>
            Questions? Call Lab IT Support at ext. 7777
        </p>
    </div>
</body>
</html>
        """
    }
)

# Template 3: HIPAA Compliance Training (All Clinical)
EmailTemplate.objects.get_or_create(
    name="Mandatory HIPAA Compliance Verification",
    defaults={
        'subject_line': "HIPAA Compliance: Annual Certification Due Today",
        'sender_name': "Compliance Department",
        'sender_email': "compliance@health-system.org",
        'difficulty_level': "HARD",
        'scenario_type': "HIPAA_COMPLIANCE",
        'target_audience': "CLINICAL_STAFF",
        'phishing_indicators': """
- Threatens compliance violation consequences
- Creates false urgency with same-day deadline
- Requests login credentials for "verification"
- Slightly modified sender domain
- Professional appearance makes it seem legitimate
        """,
        'body_html': """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto;">
    <div style="background-color: #2c3e50; color: white; padding: 20px;">
        <h2 style="margin: 0;">📋 HIPAA Compliance Office</h2>
    </div>
    
    <div style="padding: 30px; background-color: #ffffff;">
        <p>Dear Healthcare Professional,</p>
        
        <p>According to our records, your annual HIPAA compliance certification is <strong>due today</strong>. 
        Federal regulations require all clinical staff to complete this certification annually to maintain 
        their access to protected health information (PHI).</p>
        
        <div style="background-color: #fff3cd; border-left: 4px solid #ff9800; padding: 15px; margin: 20px 0;">
            <p style="margin: 0;"><strong>IMPORTANT:</strong> Failure to complete this certification 
            by 11:59 PM tonight will result in:</p>
            <ul style="margin: 10px 0;">
                <li>Immediate suspension of EMR access</li>
                <li>Compliance violation report to your supervisor</li>
                <li>Mandatory remediation training</li>
                <li>Potential disciplinary action</li>
            </ul>
        </div>
        
        <p>The certification takes approximately 5 minutes and covers:</p>
        <ul>
            <li>Patient privacy protection requirements</li>
            <li>Minimum necessary standard</li>
            <li>Breach notification procedures</li>
            <li>Security safeguards</li>
        </ul>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{{tracking_link}}" 
               style="background-color: #2c3e50; 
                      color: white; 
                      padding: 15px 40px; 
                      text-decoration: none; 
                      border-radius: 5px;
                      display: inline-block;
                      font-weight: bold;">
                Complete HIPAA Certification
            </a>
        </div>
        
        <p style="color: #666; font-size: 12px; margin-top: 30px;">
            HIPAA Compliance Office<br>
            Health System Compliance Department<br>
            For questions, contact compliance@[organization].org
        </p>
    </div>
</body>
</html>
        """
    }
)

# Template 4: Patient Portal Access Issue (Clinical Staff)
EmailTemplate.objects.get_or_create(
    name="Patient Portal Security Alert",
    defaults={
        'subject_line': "Security Alert: Unusual Activity on Your Provider Account",
        'sender_name': "MyChart Security Team",
        'sender_email': "security@mychart-alerts.com",
        'difficulty_level': "MEDIUM",
        'scenario_type': "PATIENT_PORTAL",
        'target_audience': "CLINICAL_STAFF",
        'phishing_indicators': """
- Creates false security concern
- Suspicious domain (not official MyChart)
- Requests immediate verification
- Uses fear tactic about "unusual activity"
- External security link
        """,
        'body_html': """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto;">
    <div style="background-color: #d32f2f; color: white; padding: 20px; text-align: center;">
        <h2 style="margin: 0;">⚠️ Security Alert</h2>
    </div>
    
    <div style="padding: 30px; background-color: #ffffff;">
        <p>Dear Provider,</p>
        
        <p>Our security systems have detected <strong>unusual login activity</strong> on your 
        MyChart provider account. For your protection, we have temporarily restricted access until 
        you verify your identity.</p>
        
        <div style="background-color: #ffebee; border: 2px solid #d32f2f; padding: 15px; margin: 20px 0;">
            <p style="margin: 0; color: #d32f2f;"><strong>Suspicious Activity Detected:</strong></p>
            <ul style="margin: 10px 0;">
                <li>Login attempts from unrecognized location</li>
                <li>Access to multiple patient records</li>
                <li>Date: Today at 2:47 AM</li>
            </ul>
        </div>
        
        <p>To restore your access and secure your account:</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{{tracking_link}}" 
               style="background-color: #d32f2f; 
                      color: white; 
                      padding: 15px 40px; 
                      text-decoration: none; 
                      border-radius: 5px;
                      display: inline-block;
                      font-weight: bold;">
                Verify Account Now
            </a>
        </div>
        
        <p style="color: #d32f2f;"><strong>Time Sensitive:</strong> If you don't verify within 24 hours, 
        your account will be permanently locked and require IT administrator intervention.</p>
        
        <p style="color: #666; font-size: 12px; margin-top: 30px;">
            MyChart Security Team<br>
            This is an automated security alert<br>
            Do not reply to this email
        </p>
    </div>
</body>
</html>
        """
    }
)

# Template 5: Medical Equipment Vendor (Lab Staff)
EmailTemplate.objects.get_or_create(
    name="Laboratory Equipment Calibration Notice",
    defaults={
        'subject_line': "URGENT: Lab Equipment Calibration Certificate Expiring",
        'sender_name': "Beckman Coulter Service",
        'sender_email': "service@beckman-calibration.com",
        'difficulty_level': "EASY",
        'scenario_type': "MEDICAL_VENDOR",
        'target_audience': "LAB_STAFF",
        'phishing_indicators': """
- Spoofed vendor domain (not official Beckman site)
- Creates urgency with expiring certification
- Threatens inspection failure
- Requests immediate action
- External link for "documentation"
        """,
        'body_html': """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto;">
    <div style="background-color: #0066cc; color: white; padding: 20px;">
        <h2 style="margin: 0;">🔬 Beckman Coulter Service Department</h2>
    </div>
    
    <div style="padding: 30px; background-color: #ffffff;">
        <p>Dear Laboratory Manager,</p>
        
        <p>This is an urgent notice that the calibration certificate for your laboratory equipment 
        is expiring in <strong>48 hours</strong>:</p>
        
        <div style="background-color: #e3f2fd; border-left: 4px solid #0066cc; padding: 15px; margin: 20px 0;">
            <p style="margin: 0;"><strong>Equipment Details:</strong></p>
            <ul style="margin: 10px 0;">
                <li>Device: DxH 900 Hematology Analyzer</li>
                <li>Serial Number: DXH-7849231</li>
                <li>Calibration Due: 48 hours</li>
                <li>Status: CRITICAL</li>
            </ul>
        </div>
        
        <p style="color: #d32f2f;"><strong>Regulatory Impact:</strong> Expired calibration 
        certificates may result in:</p>
        <ul>
            <li>Failed CAP/CLIA inspections</li>
            <li>Invalidated test results</li>
            <li>Laboratory shutdown</li>
            <li>Loss of accreditation</li>
        </ul>
        
        <p>Download your updated calibration certificate immediately:</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{{tracking_link}}" 
               style="background-color: #0066cc; 
                      color: white; 
                      padding: 15px 40px; 
                      text-decoration: none; 
                      border-radius: 5px;
                      display: inline-block;
                      font-weight: bold;">
                Download Calibration Certificate
            </a>
        </div>
        
        <p style="color: #666; font-size: 12px; margin-top: 30px;">
            Beckman Coulter Service Department<br>
            24/7 Technical Support: 1-800-526-3821<br>
            service@beckmancoulter.com
        </p>
    </div>
</body>
</html>
        """
    }
)

# Template 6: Pharmacy Prescription Alert (Pharmacy Staff)
EmailTemplate.objects.get_or_create(
    name="Pharmacy System - Controlled Substance Alert",
    defaults={
        'subject_line': "CRITICAL: Controlled Substance Discrepancy Detected",
        'sender_name': "Pharmacy Compliance",
        'sender_email': "rx-compliance@hospital-pharmacy.net",
        'difficulty_level': "HARD",
        'scenario_type': "PHARMACY_RX",
        'target_audience': "PHARMACY",
        'phishing_indicators': """
- Creates fear with DEA investigation threat
- Uses professional compliance language
- Suspicious sender domain
- Urgent timeline for response
- Requests login for "verification"
        """,
        'body_html': """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto;">
    <div style="background-color: #d32f2f; color: white; padding: 20px;">
        <h2 style="margin: 0;">⚕️ Pharmacy Compliance Alert</h2>
    </div>
    
    <div style="padding: 30px; background-color: #ffffff;">
        <p>CONFIDENTIAL - Pharmacy Staff Only</p>
        
        <p>Our automated system has flagged a <strong>controlled substance discrepancy</strong> 
        in your pharmacy's inventory that requires immediate attention.</p>
        
        <div style="background-color: #ffebee; border: 2px solid #d32f2f; padding: 15px; margin: 20px 0;">
            <p style="margin: 0; color: #d32f2f;"><strong>⚠️ ALERT DETAILS:</strong></p>
            <ul style="margin: 10px 0;">
                <li>Medication: Oxycodone 10mg</li>
                <li>Discrepancy: 45 tablets unaccounted</li>
                <li>Date Range: Last 72 hours</li>
                <li>Status: Pending DEA Review</li>
            </ul>
        </div>
        
        <p><strong>Regulatory Implications:</strong></p>
        <ul>
            <li>Potential DEA investigation</li>
            <li>Pharmacy license at risk</li>
            <li>Individual pharmacist license review</li>
            <li>Mandatory reporting to state board</li>
        </ul>
        
        <p>You must verify your controlled substance logs <strong>within 4 hours</strong> to 
        resolve this discrepancy before it's escalated to federal authorities.</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{{tracking_link}}" 
               style="background-color: #d32f2f; 
                      color: white; 
                      padding: 15px 40px; 
                      text-decoration: none; 
                      border-radius: 5px;
                      display: inline-block;
                      font-weight: bold;">
                Verify Controlled Substance Log
            </a>
        </div>
        
        <p style="color: #666; font-size: 12px; margin-top: 30px;">
            Pharmacy Compliance Department<br>
            This is a confidential regulatory notice<br>
            For urgent assistance: ext. 9999
        </p>
    </div>
</body>
</html>
        """
    }
)

# Template 7: Insurance Verification (Billing/Administrative)
EmailTemplate.objects.get_or_create(
    name="Insurance Verification Portal Update",
    defaults={
        'subject_line': "Action Required: Insurance Verification System Maintenance",
        'sender_name': "Revenue Cycle Management",
        'sender_email': "rcm@hospital-billing.com",
        'difficulty_level': "MEDIUM",
        'scenario_type': "INSURANCE_VERIFY",
        'target_audience': "BILLING_CODING",
        'phishing_indicators': """
- Creates urgency with system maintenance deadline
- Suspicious sender domain
- Threatens loss of access to billing systems
- Requests credential verification
- Generic greeting
        """,
        'body_html': """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto;">
    <div style="background-color: #1976d2; color: white; padding: 20px;">
        <h2 style="margin: 0;">💼 Revenue Cycle Management</h2>
    </div>
    
    <div style="padding: 30px; background-color: #ffffff;">
        <p>Dear Billing Team Member,</p>
        
        <p>The Insurance Verification Portal will undergo critical system maintenance 
        <strong>tonight at midnight</strong>. All users must re-verify their credentials 
        before the maintenance window to avoid service interruption.</p>
        
        <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0;">
            <p style="margin: 0;"><strong>Systems Affected:</strong></p>
            <ul style="margin: 10px 0;">
                <li>Insurance Eligibility Verification</li>
                <li>Prior Authorization Portal</li>
                <li>Claims Submission System</li>
                <li>Payment Posting Module</li>
            </ul>
        </div>
        
        <p><strong>Business Impact:</strong> Users who don't re-verify will be unable to:</p>
        <ul>
            <li>Check patient insurance eligibility</li>
            <li>Submit claims</li>
            <li>Process prior authorizations</li>
            <li>Access billing reports</li>
        </ul>
        
        <p>Verify your credentials now to maintain uninterrupted access:</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{{tracking_link}}" 
               style="background-color: #1976d2; 
                      color: white; 
                      padding: 15px 40px; 
                      text-decoration: none; 
                      border-radius: 5px;
                      display: inline-block;
                      font-weight: bold;">
                Verify Billing System Credentials
            </a>
        </div>
        
        <p style="color: #666; font-size: 12px; margin-top: 30px;">
            Revenue Cycle Management<br>
            IT Systems Department<br>
            Support available 24/7 at ext. 8888
        </p>
    </div>
</body>
</html>
        """
    }
)

# Template 8: COVID Health Alert (All Clinical)
EmailTemplate.objects.get_or_create(
    name="Employee Health - COVID Exposure Alert",
    defaults={
        'subject_line': "URGENT: Potential COVID-19 Exposure - Action Required",
        'sender_name': "Employee Health Services",
        'sender_email': "employeehealth@hospital-hr.com",
        'difficulty_level': "EASY",
        'scenario_type': "HEALTH_ALERT",
        'target_audience': "CLINICAL_STAFF",
        'phishing_indicators': """
- Creates health-related fear and urgency
- Suspicious sender domain
- Requests immediate personal information
- Uses current health crisis
- External screening link
        """,
        'body_html': """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto;">
    <div style="background-color: #ff6b6b; color: white; padding: 20px;">
        <h2 style="margin: 0;">🏥 Employee Health Services</h2>
    </div>
    
    <div style="padding: 30px; background-color: #ffffff;">
        <p>Dear Staff Member,</p>
        
        <p><strong>You may have been exposed to COVID-19</strong> during your shift on 
        [Date]. An employee who worked in your unit has tested positive.</p>
        
        <div style="background-color: #fff3cd; border-left: 4px solid #ff6b6b; padding: 15px; margin: 20px 0;">
            <p style="margin: 0;"><strong>⚠️ IMMEDIATE ACTION REQUIRED:</strong></p>
            <ul style="margin: 10px 0;">
                <li>Complete COVID screening questionnaire</li>
                <li>Schedule testing within 24 hours</li>
                <li>Review isolation protocols</li>
                <li>Update vaccination status</li>
            </ul>
        </div>
        
        <p><strong>Exposure Details:</strong></p>
        <ul>
            <li>Location: 3rd Floor Medical Unit</li>
            <li>Date of Exposure: [Yesterday]</li>
            <li>Duration: Extended contact</li>
            <li>PPE Status: Under review</li>
        </ul>
        
        <p>Click below to complete your COVID screening and receive testing instructions:</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{{tracking_link}}" 
               style="background-color: #ff6b6b; 
                      color: white; 
                      padding: 15px 40px; 
                      text-decoration: none; 
                      border-radius: 5px;
                      display: inline-block;
                      font-weight: bold;">
                Complete COVID Screening
            </a>
        </div>
        
        <p style="color: #d32f2f;"><strong>Note:</strong> Failure to complete screening may 
        result in restricted access to patient care areas.</p>
        
        <p style="color: #666; font-size: 12px; margin-top: 30px;">
            Employee Health Services<br>
            Occupational Health Department<br>
            24/7 Hotline: ext. 3333
        </p>
    </div>
</body>
</html>
        """
    }
)

print("✅ Successfully created 8 healthcare-specific email templates!")
print("\nTemplates created:")
print("1. Epic EMR Password Expiration (Clinical Staff)")
print("2. Laboratory Information System Update (Lab Staff)")
print("3. Mandatory HIPAA Compliance Verification (Clinical Staff)")
print("4. Patient Portal Security Alert (Clinical Staff)")
print("5. Laboratory Equipment Calibration Notice (Lab Staff)")
print("6. Controlled Substance Discrepancy Alert (Pharmacy Staff)")
print("7. Insurance Verification Portal Update (Billing Staff)")
print("8. COVID-19 Exposure Alert (Clinical Staff)")
print("\nThese templates can now be used in phishing simulation campaigns!")
