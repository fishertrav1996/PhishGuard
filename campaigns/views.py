from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from email.utils import formataddr
from .models import CampaignTarget, Campaign, EmailTemplate
from orgs.models import Organization, Employee
from orgs.permissions import (
    get_user_organizations,
    require_campaign_access,
    user_can_manage_campaigns
)

# Constants for email status choices
EMAIL_STATUS_CHOICES = ['SENT', 'OPENED', 'CLICKED', 'REPORTED']

@csrf_exempt  # Tracking links in emails won't have CSRF tokens
def track_click(request, token):
    """
    Track when an employee clicks a phishing simulation link.
    Records the click timestamp and redirects to educational landing page.
    """
    try:
        target = get_object_or_404(CampaignTarget, unique_tracking_token=token)
        
        # Record the click if not already clicked
        if not target.link_clicked_at:
            target.link_clicked_at = timezone.now()
            target.status = 'CLICKED'
            target.save()
        
        # Assign remediation if not already assigned
        if not target.remediation_assigned_at:
            target.remediation_assigned_at = timezone.now()
            target.save()
        
        # Redirect to educational landing page
        return render(request, 'campaigns/phishing_revealed.html', {
            'employee_name': target.employee.first_name,
            'campaign_name': target.campaign.name,
            'tracking_token': token,
            'remediation_completed': target.remediation_completed_at is not None,
            'remediation_completed_at': target.remediation_completed_at,
        })
        
    except CampaignTarget.DoesNotExist:
        return HttpResponse("Invalid tracking link", status=404)


@csrf_exempt  # Training completion doesn't require authentication
def complete_remediation(request, token):
    """
    Mark remediation training as complete when employee acknowledges training.
    """
    if request.method != 'POST':
        return HttpResponse("Method not allowed", status=405)
    
    try:
        target = get_object_or_404(CampaignTarget, unique_tracking_token=token)
        
        # Verify acknowledgment checkbox was checked
        if not request.POST.get('acknowledgment'):
            return HttpResponse("Acknowledgment is required", status=400)
        
        # Mark remediation as complete if not already done
        if not target.remediation_completed_at:
            target.remediation_completed_at = timezone.now()
            target.save()
        
        # Redirect back to phishing revealed page with success message
        return render(request, 'campaigns/phishing_revealed.html', {
            'employee_name': target.employee.first_name,
            'campaign_name': target.campaign.name,
            'tracking_token': token,
            'remediation_completed': True,
            'remediation_completed_at': target.remediation_completed_at,
        })
        
    except CampaignTarget.DoesNotExist:
        return HttpResponse("Invalid tracking link", status=404)


@login_required
def campaign_list(request):
    """List all campaigns for user's organizations"""
    # Get all organizations user belongs to
    user_orgs = get_user_organizations(request.user)
    
    if not user_orgs.exists():
        messages.error(request, "You must create or join an organization first.")
        return redirect('new_org')
    
    # Get campaigns from all user's organizations
    campaigns = Campaign.objects.filter(
        organization__in=user_orgs
    ).select_related('organization', 'email_template', 'created_by')
    
    return render(request, 'campaigns/campaign_list.html', {
        'campaigns': campaigns,
        'user_organizations': user_orgs,
    })


@login_required
@require_campaign_access
def campaign_detail(request, campaign_uuid):
    """View campaign details and statistics"""
    # campaign, organization, and org_membership added by decorator
    campaign = request.campaign
    
    # Get statistics
    targets = campaign.targets.all()
    total_targets = targets.count()
    sent_count = targets.filter(status__in=EMAIL_STATUS_CHOICES).count()
    clicked_count = targets.filter(status='CLICKED').count()
    
    # Calculate remediation statistics
    remediation_assigned_count = targets.filter(remediation_assigned_at__isnull=False).count()
    remediation_completed_count = targets.filter(remediation_completed_at__isnull=False).count()
    remediation_pending_count = targets.filter(
        remediation_assigned_at__isnull=False,
        remediation_completed_at__isnull=True
    ).count()
    
    # Calculate percentages
    click_rate = calculate_click_rate(clicked_count, sent_count)
    remediation_assigned_percentage = (remediation_assigned_count / clicked_count * 100) if clicked_count > 0 else 0
    remediation_completion_rate = (remediation_completed_count / remediation_assigned_count * 100) if remediation_assigned_count > 0 else 0
    
    return render(request, 'campaigns/campaign_detail.html', {
        'campaign': campaign,
        'targets': targets,
        'total_targets': total_targets,
        'sent_count': sent_count,
        'clicked_count': clicked_count,
        'click_rate': click_rate,
        'remediation_assigned_count': remediation_assigned_count,
        'remediation_completed_count': remediation_completed_count,
        'remediation_pending_count': remediation_pending_count,
        'remediation_assigned_percentage': remediation_assigned_percentage,
        'remediation_completion_rate': remediation_completion_rate,
        'user_membership': request.org_membership,
    })


@login_required
def create_campaign(request):
    """Create a new phishing campaign"""
    # Get user's organizations where they can manage campaigns
    user_orgs = get_user_organizations(request.user)
    
    if not user_orgs.exists():
        messages.error(request, "You must create or join an organization first.")
        return redirect('new_org')
    
    # For now, use first org or get from query param
    org_id = request.GET.get('org_id') or request.POST.get('org_id')
    if org_id:
        organization = get_object_or_404(Organization, id=org_id, id__in=user_orgs.values_list('id', flat=True))
    else:
        organization = user_orgs.first()
    
    # Check if user can manage campaigns for this org
    if not user_can_manage_campaigns(request.user, organization):
        messages.error(request, "You don't have permission to create campaigns for this organization.")
        return redirect('campaigns:campaign_list')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        template_id = request.POST.get('email_template')
        employee_ids = request.POST.getlist('employees')
        
        # Create campaign
        template = EmailTemplate.objects.get(id=template_id) if template_id else None
        campaign = Campaign.objects.create(
            organization=organization,
            name=name,
            description=description,
            email_template=template,
            created_by=request.user,
        )
        
        # Create targets for selected employees
        for id in employee_ids:
            employee = Employee.objects.get(id=id, organization=organization)
            CampaignTarget.objects.create(
                campaign=campaign,
                employee=employee
            )
        
        messages.success(request, f"Campaign '{name}' created successfully!")
        return redirect('campaigns:campaign_detail', campaign_uuid=campaign.uuid)
    
    # GET request - show form
    elif request.method == 'GET':
        templates = EmailTemplate.objects.all()
        employees = organization.employees.all()
    
        return render(request, 'campaigns/create_campaign.html', {
            'templates': templates,
            'employees': employees,
            'organization': organization,
            'user_organizations': user_orgs,
        })
    else:
        return HttpResponse("Method not allowed", status=405)


@login_required
@require_campaign_access
def send_campaign(request, campaign_uuid):
    """Send phishing emails for a campaign"""
    campaign = request.campaign
    
    # Verify user can manage campaigns
    if not request.org_membership.can_manage_campaigns():
        messages.error(request, "You don't have permission to send campaigns.")
        return redirect('campaigns:campaign_list')
    
    if request.method == 'POST':
        targets = campaign.targets.filter(status='PENDING')
        sent_count = 0
        
        for target in targets:
            try:
                # Build tracking URL
                tracking_url = request.build_absolute_uri(
                    f'/campaigns/track/{target.unique_tracking_token}/'
                )
                
                # Replace placeholder in email template
                email_body = campaign.email_template.body_html.replace(
                    '{{tracking_link}}', 
                    tracking_url
                )
                
                # Properly format sender with name (handles commas and special chars)
                from_email = formataddr((
                    campaign.email_template.sender_name,
                    settings.DEFAULT_FROM_EMAIL
                ))
                
                # Send email
                send_mail(
                    subject=campaign.email_template.subject_line,
                    message='',  # Plain text version
                    html_message=email_body,
                    from_email=from_email,
                    recipient_list=[target.employee.email],
                    fail_silently=False,
                )
                
                # Update target status
                target.sent_at = timezone.now()
                target.status = 'SENT'
                target.save()
                sent_count += 1
                
            except Exception as e:
                messages.warning(request, f"Failed to send to {target.employee.email}: {str(e)}")
        
        # Update campaign status
        if sent_count > 0:
            campaign.status = 'ACTIVE'
            campaign.save()
            messages.success(request, f"Successfully sent {sent_count} phishing simulation emails!")
        else:
            messages.error(request, "No emails were sent.")
        
        return redirect('campaigns:campaign_detail', campaign_uuid=campaign.uuid)
    
    # GET request - show confirmation page
    elif request.method == 'GET':
        pending_count = campaign.targets.filter(status='PENDING').count()
        return render(request, 'campaigns/send_campaign.html', {
            'campaign': campaign,
            'pending_count': pending_count,
        })
    else:
        return HttpResponse("Method not allowed", status=405)


def calculate_click_rate(clicked_count, sent_count):
    """Helper function to calculate click rate for a campaign"""
    if sent_count == 0:
        return 0.0
    return (clicked_count / sent_count) * 100

