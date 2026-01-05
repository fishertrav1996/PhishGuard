from django.contrib import admin
from .models import EmailTemplate, Campaign, CampaignTarget, ComplianceReport


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'scenario_type', 'target_audience', 'difficulty_level', 'created_at']
    list_filter = ['scenario_type', 'target_audience', 'difficulty_level', 'created_at']
    search_fields = ['name', 'subject_line', 'sender_name']
    ordering = ['-created_at']
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'difficulty_level', 'scenario_type', 'target_audience')
        }),
        ('Email Content', {
            'fields': ('subject_line', 'sender_name', 'sender_email', 'body_html')
        }),
        ('Educational Content', {
            'fields': ('phishing_indicators',),
            'description': 'Description of red flags to help educate employees after the simulation'
        }),
    )


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'created_at', 'organization']
    search_fields = ['name', 'description', 'organization__organization_name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CampaignTarget)
class CampaignTargetAdmin(admin.ModelAdmin):
    list_display = ['employee', 'campaign', 'status', 'sent_at', 'link_clicked_at']
    list_filter = ['status', 'sent_at', 'link_clicked_at']
    search_fields = ['employee__email', 'employee__first_name', 'employee__last_name', 'campaign__name']
    readonly_fields = ['unique_tracking_token', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(ComplianceReport)
class ComplianceReportAdmin(admin.ModelAdmin):
    list_display = ['organization', 'report_type', 'period_start', 'period_end', 'total_campaigns', 'overall_click_rate', 'generated_at']
    list_filter = ['report_type', 'generated_at', 'organization']
    search_fields = ['organization__organization_name']
    readonly_fields = ['uuid', 'generated_at', 'file_path']
    ordering = ['-generated_at']
    
    fieldsets = (
        ('Report Information', {
            'fields': ('uuid', 'organization', 'report_type', 'period_start', 'period_end')
        }),
        ('Frameworks', {
            'fields': ('frameworks',)
        }),
        ('Statistics', {
            'fields': ('total_campaigns', 'total_employees_trained', 'overall_click_rate', 'remediation_completion_rate')
        }),
        ('File & Metadata', {
            'fields': ('file_path', 'generated_by', 'generated_at')
        }),
    )

