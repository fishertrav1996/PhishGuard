from django.db import models
from django.contrib.auth.models import User
from orgs.models import Organization, Employee
import uuid

# Constants for choice fields
TEMPLATE_DIFFICULTY_CHOICES = [
        ('EASY', 'Easy'),
        ('MEDIUM', 'Medium'),
        ('HARD', 'Hard'),
    ]
CAMPAIGN_STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SCHEDULED', 'Scheduled'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
    ]
TARGET_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('OPENED', 'Opened'),
        ('CLICKED', 'Clicked'),
        ('REPORTED', 'Reported'),
    ]

class EmailTemplate(models.Model):
    """Reusable phishing email templates"""
    
    name = models.CharField(max_length=200)
    subject_line = models.CharField(max_length=300)
    body_html = models.TextField(help_text="HTML content with {{tracking_link}} placeholder")
    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField()
    phishing_indicators = models.TextField(
        blank=True,
        help_text="Description of phishing red flags in this template"
    )
    difficulty_level = models.CharField(max_length=10, choices=TEMPLATE_DIFFICULTY_CHOICES, default='MEDIUM')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Campaign(models.Model):
    """Phishing simulation campaign"""
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='campaigns'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=CAMPAIGN_STATUS_CHOICES, default='DRAFT')
    scheduled_send_date = models.DateTimeField(null=True, blank=True)
    email_template = models.ForeignKey(
        EmailTemplate,
        on_delete=models.SET_NULL,
        null=True,
        related_name='campaigns'
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.organization.organization_name}"
    
    class Meta:
        ordering = ['-created_at']


class CampaignTarget(models.Model):
    """Tracks individual employee's interaction with campaign"""
    
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='targets'
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='campaign_targets'
    )
    unique_tracking_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    # Tracking timestamps
    sent_at = models.DateTimeField(null=True, blank=True)
    email_opened_at = models.DateTimeField(null=True, blank=True)
    link_clicked_at = models.DateTimeField(null=True, blank=True)
    reported_at = models.DateTimeField(null=True, blank=True)
    
    # Remediation tracking
    remediation_assigned_at = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="When remediation training was assigned after clicking phishing link."
    )
    remediation_completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When employee completed remediation acknowledgment."
    )
    
    status = models.CharField(max_length=20, choices=TARGET_STATUS_CHOICES, default='PENDING')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.employee.email} - {self.campaign.name}"
    
    class Meta:
        unique_together = ['campaign', 'employee']
        ordering = ['-created_at']


class ComplianceReport(models.Model):
    """Generated compliance reports for audit trail"""
    
    REPORT_TYPE_CHOICES = [
        ('QUARTERLY', 'Quarterly Compliance Report'),
        ('ANNUAL', 'Annual Security Training Report'),
        ('CAMPAIGN', 'Campaign-Specific Report'),
        ('AUDIT', 'Audit-Ready Package'),
    ]
    
    # Compliance frameworks included in report
    FRAMEWORK_CHOICES = [
        ('HIPAA', 'HIPAA Security Rule § 164.308(a)(5)'),
        ('HITECH', 'HITECH Act'),
        ('HITRUST', 'HITRUST CSF Control 02.g'),
        ('NIST', 'NIST Cybersecurity Framework PR.AT-1'),
        ('STATE_LAWS', 'State Breach Notification Laws'),
    ]
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='compliance_reports'
    )
    
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES, default='QUARTERLY')
    
    # Time period covered by report
    period_start = models.DateField(help_text="Start date of reporting period")
    period_end = models.DateField(help_text="End date of reporting period")
    
    # Compliance frameworks included (stored as comma-separated values)
    frameworks = models.CharField(
        max_length=200,
        default='HIPAA,HITECH,HITRUST,NIST,STATE_LAWS',
        help_text="Comma-separated list of included frameworks"
    )
    
    # File storage
    file_path = models.CharField(max_length=500, help_text="Path to generated PDF file")
    
    # Metadata
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    # Summary statistics (stored for quick access without re-parsing PDF)
    total_campaigns = models.IntegerField(default=0)
    total_employees_trained = models.IntegerField(default=0)
    overall_click_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    remediation_completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.get_report_type_display()} - {self.organization.organization_name} ({self.period_start} to {self.period_end})"
    
    def get_frameworks_list(self):
        """Return list of framework codes"""
        return self.frameworks.split(',') if self.frameworks else []
    
    def get_frameworks_display(self):
        """Return human-readable list of frameworks"""
        framework_dict = dict(self.FRAMEWORK_CHOICES)
        return [framework_dict.get(code, code) for code in self.get_frameworks_list()]
    
    class Meta:
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['organization', '-generated_at']),
        ]
