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

class Organization(models.Model):
    # Model fields
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    organization_name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE 
    )
    organization_type = models.CharField(max_length=20, choices=HEALTHCARE_ORG_TYPES, default='OTHER')
    subscription_is_active = models.BooleanField(default=False)
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_TYPES, default='FREE')
    website = models.URLField()
    street_address_1 = models.CharField(max_length=255)
    street_address_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Model methods
    def __str__(self):
        return self.organization_name
    
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