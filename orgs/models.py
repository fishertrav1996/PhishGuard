from django.db import models
from django.conf import settings
import uuid

# List for healthcare oganization types
HEALTHCARE_ORG_TYPES = [
    ('HOSPITAL', 'Hospital'),
    ('CLINIC', 'Clinic'),
    ('PHARMACY', 'Pharmacy'),
    ('LABORATORY', 'Laboratory'),
    ('OTHER', 'Other')
]

# List for subscription types
SUBSCRIPTION_TYPES = [
    ('FREE', 'Free'),
    ('PREMIUM', 'Premium')
]

EMPLOYEE_ROLE_TYPES = [
    ('ADMIN', 'Admin'),
    ('STAFF', 'Staff'),
    ('OTHER', 'OTHER')
]

# US States and Territories
US_STATES = [
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
    ('AS', 'American Samoa'),
    ('GU', 'Guam'),
    ('MP', 'Northern Mariana Islands'),
    ('PR', 'Puerto Rico'),
    ('VI', 'U.S. Virgin Islands'),
]

class Organization(models.Model):
    # Model fields
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    organization_name = models.CharField(max_length=100)
    organization_type = models.CharField(max_length=20, choices=HEALTHCARE_ORG_TYPES, default='OTHER')
    subscription_is_active = models.BooleanField(default=False)
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_TYPES, default='FREE')
    website = models.URLField()
    street_address_1 = models.CharField(max_length=255)
    street_address_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100, choices=US_STATES)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='United States')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Model methods
    def __str__(self):
        return self.organization_name
    
class OrganizationMembership(models.Model):
    """
    Junction table linking Users to Organizations with role-based permissions.
    Supports multiple admins per org and users belonging to multiple orgs.
    """
    
    ROLE_CHOICES = [
        ('OWNER', 'Owner'),           # Full control + billing + delete org
        ('ADMIN', 'Admin'),           # Campaign management + reports + settings
        ('MEMBER', 'Member'),         # View campaigns and reports only
        ('BILLING', 'Billing Admin'), # Subscription management only
    ]
    
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='org_memberships'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='MEMBER')
    
    # Invitation/audit trail
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invitations_sent'
    )
    invited_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['organization', 'user']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['organization', 'role']),
        ]
        verbose_name = 'Organization Membership'
        verbose_name_plural = 'Organization Memberships'
    
    def __str__(self):
        return f"{self.user.username} - {self.organization.organization_name} ({self.role})"
    
    def can_manage_campaigns(self):
        """Check if user can create/edit campaigns"""
        return self.role in ['OWNER', 'ADMIN'] and self.is_active
    
    def can_manage_settings(self):
        """Check if user can modify org settings"""
        return self.role in ['OWNER', 'ADMIN'] and self.is_active
    
    def can_manage_billing(self):
        """Check if user can manage subscription"""
        return self.role in ['OWNER', 'BILLING'] and self.is_active
    
    def can_export_reports(self):
        """Check if user can export compliance reports"""
        return self.role in ['OWNER', 'ADMIN'] and self.is_active
    
    def is_owner(self):
        """Check if user is the organization owner"""
        return self.role == 'OWNER' and self.is_active


class Employee(models.Model):
    # Model fields
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='employees')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=EMPLOYEE_ROLE_TYPES, default='STAFF')
    position = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Model methods
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.organization.organization_name}"