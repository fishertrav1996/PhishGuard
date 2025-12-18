from django.contrib import admin
from .models import EmailTemplate, Campaign, CampaignTarget


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject_line', 'difficulty_level', 'created_at']
    list_filter = ['difficulty_level', 'created_at']
    search_fields = ['name', 'subject_line']
    ordering = ['-created_at']


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

