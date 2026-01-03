"""
Test script to verify the membership system implementation.
Run with: python manage.py shell < test_membership.py
"""

from django.contrib.auth.models import User
from orgs.models import Organization, OrganizationMembership, Employee
from orgs.permissions import (
    get_user_organizations,
    get_user_membership,
    user_can_manage_campaigns,
    user_is_owner
)

print("=" * 60)
print("TESTING ORGANIZATION MEMBERSHIP SYSTEM")
print("=" * 60)

# Create test user
print("\n1. Creating test user...")
user, created = User.objects.get_or_create(
    username='test_owner',
    defaults={
        'email': 'owner@test.com',
        'first_name': 'Test',
        'last_name': 'Owner'
    }
)
if created:
    user.set_password('testpass123')
    user.save()
print(f"   ✓ User: {user.username}")

# Create test organization
print("\n2. Creating test organization...")
org, created = Organization.objects.get_or_create(
    organization_name='Test Hospital',
    defaults={
        'organization_type': 'HOSPITAL',
        'subscription_type': 'FREE',
        'subscription_is_active': False,
        'website': 'https://test-hospital.com',
        'street_address_1': '123 Test St',
        'city': 'Test City',
        'state_province': 'Test State',
        'postal_code': '12345',
        'country': 'Test Country'
    }
)
print(f"   ✓ Organization: {org.organization_name}")

# Create membership
print("\n3. Creating OWNER membership...")
membership, created = OrganizationMembership.objects.get_or_create(
    organization=org,
    user=user,
    defaults={
        'role': 'OWNER',
        'is_active': True
    }
)
print(f"   ✓ Membership: {membership}")

# Test permission functions
print("\n4. Testing permission functions...")
user_orgs = get_user_organizations(user)
print(f"   • get_user_organizations: {user_orgs.count()} org(s)")

mem = get_user_membership(user, org)
print(f"   • get_user_membership: {mem.role if mem else 'None'}")

can_manage = user_can_manage_campaigns(user, org)
print(f"   • user_can_manage_campaigns: {can_manage}")

is_owner = user_is_owner(user, org)
print(f"   • user_is_owner: {is_owner}")

# Test membership methods
print("\n5. Testing membership methods...")
print(f"   • can_manage_campaigns: {membership.can_manage_campaigns()}")
print(f"   • can_manage_settings: {membership.can_manage_settings()}")
print(f"   • can_manage_billing: {membership.can_manage_billing()}")
print(f"   • can_export_reports: {membership.can_export_reports()}")
print(f"   • is_owner: {membership.is_owner()}")

# Create a second user as ADMIN
print("\n6. Creating admin user...")
admin_user, created = User.objects.get_or_create(
    username='test_admin',
    defaults={
        'email': 'admin@test.com',
        'first_name': 'Test',
        'last_name': 'Admin'
    }
)
if created:
    admin_user.set_password('testpass123')
    admin_user.save()

admin_mem, created = OrganizationMembership.objects.get_or_create(
    organization=org,
    user=admin_user,
    defaults={
        'role': 'ADMIN',
        'is_active': True,
        'invited_by': user
    }
)
print(f"   ✓ Admin membership: {admin_mem}")
print(f"   • Can manage campaigns: {admin_mem.can_manage_campaigns()}")
print(f"   • Is owner: {admin_mem.is_owner()}")
print(f"   • Can manage billing: {admin_mem.can_manage_billing()}")

# Show all memberships
print("\n7. All memberships for organization:")
for m in org.memberships.all():
    print(f"   • {m.user.username} - {m.role} (active: {m.is_active})")

print("\n" + "=" * 60)
print("✓ MEMBERSHIP SYSTEM TEST COMPLETE")
print("=" * 60)
