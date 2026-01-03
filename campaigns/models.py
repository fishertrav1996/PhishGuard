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
