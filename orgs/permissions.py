"""
Permission utilities and decorators for organization membership-based access control.
"""
from functools import wraps
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Organization, OrganizationMembership


def get_user_organizations(user):
    """
    Get all organizations a user belongs to.
    
    Args:
        user: Django User instance
    
    Returns:
        QuerySet of Organization objects
    """
    if not user.is_authenticated:
        return Organization.objects.none()
    
    return Organization.objects.filter(
        memberships__user=user,
        memberships__is_active=True
    ).distinct()


def get_user_membership(user, organization):
    """
    Get a user's membership for a specific organization.
    
    Args:
        user: Django User instance
        organization: Organization instance
    
    Returns:
        OrganizationMembership instance or None
    """
    if not user.is_authenticated:
        return None
    
    try:
        return OrganizationMembership.objects.get(
            user=user,
            organization=organization,
            is_active=True
        )
    except OrganizationMembership.DoesNotExist:
        return None


def user_can_manage_campaigns(user, organization):
    """
    Check if user can create/edit campaigns for an organization.
    
    Args:
        user: Django User instance
        organization: Organization instance
    
    Returns:
        bool
    """
    membership = get_user_membership(user, organization)
    return membership and membership.can_manage_campaigns()


def user_can_manage_settings(user, organization):
    """
    Check if user can modify organization settings.
    
    Args:
        user: Django User instance
        organization: Organization instance
    
    Returns:
        bool
    """
    membership = get_user_membership(user, organization)
    return membership and membership.can_manage_settings()


def user_can_export_reports(user, organization):
    """
    Check if user can export compliance reports.
    
    Args:
        user: Django User instance
        organization: Organization instance
    
    Returns:
        bool
    """
    membership = get_user_membership(user, organization)
    return membership and membership.can_export_reports()


def user_is_owner(user, organization):
    """
    Check if user is the owner of an organization.
    
    Args:
        user: Django User instance
        organization: Organization instance
    
    Returns:
        bool
    """
    membership = get_user_membership(user, organization)
    return membership and membership.is_owner()


def require_org_membership(*allowed_roles):
    """
    Decorator to require organization membership with specific roles.
    
    Usage:
        @require_org_membership('OWNER', 'ADMIN')
        def my_view(request, org_uuid):
            ...
    
    The view must accept 'org_uuid', 'org_id', or 'organization_id' as a parameter.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Extract organization identifier from URL kwargs
            org_identifier = kwargs.get('org_uuid') or kwargs.get('org_id') or kwargs.get('organization_id')
            
            if not org_identifier:
                messages.error(request, "Organization not specified.")
                return redirect('core:home')
            
            # Get the organization (handle both UUID and ID)
            try:
                organization = Organization.objects.get(uuid=org_identifier)
            except (Organization.DoesNotExist, ValueError):
                try:
                    organization = Organization.objects.get(id=org_identifier)
                except Organization.DoesNotExist:
                    messages.error(request, "Organization not found.")
                    return redirect('core:home')
            
            # Get user's membership
            membership = get_user_membership(request.user, organization)
            
            if not membership:
                messages.error(request, "You don't have access to this organization.")
                return redirect('core:home')
            
            if allowed_roles and membership.role not in allowed_roles:
                messages.error(request, f"You need {' or '.join(allowed_roles)} access for this action.")
                return redirect('orgs:list_employees', org_uuid=organization.uuid)
            
            # Add membership to request for convenience
            request.org_membership = membership
            request.organization = organization
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def require_campaign_access(view_func):
    """
    Decorator to verify user has access to a campaign.
    
    Usage:
        @require_campaign_access
        def campaign_detail(request, campaign_uuid):
            # request.organization and request.org_membership will be available
            ...
    
    The view must accept 'campaign_uuid' or 'campaign_id' as a parameter.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        from campaigns.models import Campaign
        
        # Extract campaign identifier
        campaign_uuid = kwargs.get('campaign_uuid') or kwargs.get('campaign_id')
        
        if not campaign_uuid:
            messages.error(request, "Campaign not specified.")
            return redirect('campaigns:campaign_list')
        
        # Get the campaign
        campaign = get_object_or_404(Campaign, uuid=campaign_uuid)
        
        # Check membership
        membership = get_user_membership(request.user, campaign.organization)
        
        if not membership:
            messages.error(request, "You don't have access to this campaign.")
            return redirect('campaigns:campaign_list')
        
        # Add to request for convenience
        request.org_membership = membership
        request.organization = campaign.organization
        request.campaign = campaign
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
