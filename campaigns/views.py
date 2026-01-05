from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotAllowed, FileResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string
from django.db.models import Count, Q
from email.utils import formataddr
from weasyprint import HTML
import os
from datetime import datetime, timedelta
from .models import CampaignTarget, Campaign, EmailTemplate, ComplianceReport
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
    
    # For now, use first org or get from query param
    org_id = request.GET.get('org_id')
    if org_id:
        organization = get_object_or_404(Organization, id=org_id, id__in=user_orgs.values_list('id', flat=True))
    else:
        organization = user_orgs.first()
    
    campaigns = Campaign.objects.filter(organization=organization).order_by('-created_at')
    
    # Add subscription status to context
    can_create_campaign = organization.can_create_campaign()
    campaigns_remaining = None
    if organization.subscription_tier == 'FREE_TRIAL':
        campaigns_remaining = 1 - organization.trial_campaigns_used
    
    return render(request, 'campaigns/campaign_list.html', {
        'campaigns': campaigns,
        'organization': organization,
        'user_organizations': user_orgs,
        'can_create_campaign': can_create_campaign,
        'campaigns_remaining': campaigns_remaining,
        'subscription_tier': organization.get_subscription_tier_display(),
        'requires_upgrade': organization.requires_upgrade(),
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
    
    # Check if organization can create campaigns (subscription limits)
    if not organization.can_create_campaign():
        if organization.is_trial_expired():
            messages.error(request, "Your free trial campaign has been used. Please upgrade to continue creating campaigns.")
            return redirect('campaigns:campaign_list')  # TODO: Redirect to subscription page
        elif organization.subscription_status in ['CANCELED', 'PAST_DUE']:
            messages.error(request, "Your subscription is not active. Please update your billing information.")
            return redirect('campaigns:campaign_list')  # TODO: Redirect to billing page
        else:
            messages.error(request, "You have reached your campaign limit for this subscription tier.")
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
        
        # Increment trial campaigns counter if on free trial
        if organization.subscription_tier == 'FREE_TRIAL':
            organization.trial_campaigns_used += 1
            organization.save()
        
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


# ============================================================================
# COMPLIANCE REPORTING VIEWS
# ============================================================================

@login_required
def generate_compliance_report(request, org_uuid):
    """Generate a quarterly compliance report for an organization"""
    organization = get_object_or_404(Organization, uuid=org_uuid)
    
    # Check if user can manage this organization
    if not user_can_manage_campaigns(request.user, organization):
        messages.error(request, "You don't have permission to generate reports for this organization.")
        return redirect('campaigns:campaign_list')
    
    if request.method == 'POST':
        # Get form data
        report_type = request.POST.get('report_type', 'QUARTERLY')
        period_start = request.POST.get('period_start')
        period_end = request.POST.get('period_end')
        frameworks = request.POST.getlist('frameworks')
        
        # Validate dates
        try:
            period_start_date = datetime.strptime(period_start, '%Y-%m-%d').date()
            period_end_date = datetime.strptime(period_end, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            return redirect('campaigns:generate_report', org_uuid=org_uuid)
        
        # Get campaigns in period
        campaigns = Campaign.objects.filter(
            organization=organization,
            created_at__date__gte=period_start_date,
            created_at__date__lte=period_end_date
        ).select_related('email_template')
        
        # Calculate statistics
        campaign_stats = []
        total_targets = 0
        total_sent = 0
        total_clicked = 0
        remediation_assigned = 0
        remediation_completed = 0
        unique_employees = set()
        
        for campaign in campaigns:
            targets = campaign.targets.all()
            targets_count = targets.count()
            sent_count = targets.filter(sent_at__isnull=False).count()
            clicked_count = targets.filter(link_clicked_at__isnull=False).count()
            
            campaign_stats.append({
                'name': campaign.name,
                'created_at': campaign.created_at,
                'total_targets': targets_count,
                'sent_count': sent_count,
                'clicked_count': clicked_count,
                'click_rate': calculate_click_rate(clicked_count, sent_count)
            })
            
            total_targets += targets_count
            total_sent += sent_count
            total_clicked += clicked_count
            
            # Track unique employees
            for target in targets:
                unique_employees.add(target.employee_id)
                if target.remediation_assigned_at:
                    remediation_assigned += 1
                if target.remediation_completed_at:
                    remediation_completed += 1
        
        # Calculate overall rates
        overall_click_rate = calculate_click_rate(total_clicked, total_sent)
        remediation_completion_rate = calculate_click_rate(remediation_completed, remediation_assigned)
        remediation_assigned_pct = calculate_click_rate(remediation_assigned, total_clicked)
        remediation_pending = remediation_assigned - remediation_completed
        remediation_pending_pct = calculate_click_rate(remediation_pending, remediation_assigned)
        
        # Prepare context for template
        context = {
            'organization': organization,
            'report_type_display': dict(ComplianceReport.REPORT_TYPE_CHOICES).get(report_type),
            'period_start': period_start_date,
            'period_end': period_end_date,
            'report_date': timezone.now(),
            'generated_by': request.user,
            'frameworks': frameworks,
            'training_frequency': 'Quarterly',  # Can be made configurable
            
            # Summary metrics
            'total_campaigns': campaigns.count(),
            'total_employees_trained': len(unique_employees),
            'overall_click_rate': round(overall_click_rate, 2),
            'remediation_completion_rate': round(remediation_completion_rate, 2),
            
            # Campaign details
            'campaigns': campaign_stats,
            
            # Remediation details
            'total_clicked': total_clicked,
            'remediation_assigned': remediation_assigned,
            'remediation_completed': remediation_completed,
            'remediation_pending': remediation_pending,
            'remediation_assigned_pct': round(remediation_assigned_pct, 2),
            'remediation_pending_pct': round(remediation_pending_pct, 2),
        }
        
        # Render HTML template
        html_string = render_to_string('campaigns/compliance_report_pdf.html', context)
        
        # Generate PDF
        pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
        
        # Create file storage directory
        report_dir = os.path.join(
            settings.MEDIA_ROOT,
            'compliance_reports',
            str(organization.uuid),
            str(period_start_date.year),
            f'Q{((period_start_date.month-1)//3)+1}'
        )
        os.makedirs(report_dir, exist_ok=True)
        
        # Save PDF file
        filename = f'compliance_report_{period_start_date.strftime("%Y%m%d")}_{period_end_date.strftime("%Y%m%d")}.pdf'
        file_path = os.path.join(report_dir, filename)
        
        with open(file_path, 'wb') as f:
            f.write(pdf_file)
        
        # Create database record
        report = ComplianceReport.objects.create(
            organization=organization,
            report_type=report_type,
            period_start=period_start_date,
            period_end=period_end_date,
            frameworks=','.join(frameworks),
            file_path=file_path,
            generated_by=request.user,
            total_campaigns=campaigns.count(),
            total_employees_trained=len(unique_employees),
            overall_click_rate=round(overall_click_rate, 2),
            remediation_completion_rate=round(remediation_completion_rate, 2)
        )
        
        messages.success(request, f"Compliance report generated successfully!")
        # Redirect to list with download parameter
        return redirect(f"{reverse('campaigns:list_reports', kwargs={'org_uuid': organization.uuid})}?download={report.uuid}")
    
    elif request.method == 'GET':
        # Suggest current quarter dates
        today = timezone.now().date()
        quarter_start = datetime(today.year, ((today.month-1)//3)*3+1, 1).date()
        quarter_end = today
        
        return render(request, 'campaigns/generate_compliance_report.html', {
            'organization': organization,
            'suggested_start': quarter_start,
            'suggested_end': quarter_end,
            'framework_choices': ComplianceReport.FRAMEWORK_CHOICES,
        })
    
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
def list_compliance_reports(request, org_uuid):
    """List all compliance reports for an organization"""
    organization = get_object_or_404(Organization, uuid=org_uuid)
    
    # Check if user can view this organization's reports
    if not user_can_manage_campaigns(request.user, organization):
        messages.error(request, "You don't have permission to view reports for this organization.")
        return redirect('campaigns:campaign_list')
    
    if request.method == 'GET':
        reports = ComplianceReport.objects.filter(organization=organization).order_by('-generated_at')
        
        return render(request, 'campaigns/compliance_reports_list.html', {
            'organization': organization,
            'reports': reports,
        })
    else:
        return HttpResponseNotAllowed(['GET'])


@login_required
def download_compliance_report(request, report_uuid):
    """Download a compliance report PDF"""
    report = get_object_or_404(ComplianceReport, uuid=report_uuid)
    
    # Check if user can access this report
    if not user_can_manage_campaigns(request.user, report.organization):
        messages.error(request, "You don't have permission to access this report.")
        return redirect('campaigns:campaign_list')
    
    if request.method == 'GET':
        # Check if file exists
        if not os.path.exists(report.file_path):
            messages.error(request, "Report file not found. It may have been deleted.")
            return redirect('campaigns:list_reports', org_uuid=report.organization.uuid)
        
        # Serve PDF file
        response = FileResponse(
            open(report.file_path, 'rb'),
            content_type='application/pdf'
        )
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(report.file_path)}"'
        return response
    else:
        return HttpResponseNotAllowed(['GET'])


@login_required
def delete_compliance_report(request, report_uuid):
    """Delete a compliance report"""
    report = get_object_or_404(ComplianceReport, uuid=report_uuid)
    
    # Check if user can delete this report
    if not user_can_manage_campaigns(request.user, report.organization):
        messages.error(request, "You don't have permission to delete this report.")
        return redirect('campaigns:campaign_list')
    
    if request.method == 'POST':
        org_uuid = report.organization.uuid
        
        # Delete file
        if os.path.exists(report.file_path):
            os.remove(report.file_path)
        
        # Delete database record
        report.delete()
        
        messages.success(request, "Compliance report deleted successfully.")
        return redirect('campaigns:list_reports', org_uuid=org_uuid)
    
    elif request.method == 'GET':
        return render(request, 'campaigns/confirm_delete_report.html', {
            'report': report,
        })
    
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

