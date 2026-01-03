from django.contrib import admin
from .models import Organization, Employee, OrganizationMembership


@admin.register(OrganizationMembership)
class OrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'role', 'is_active', 'invited_at')
    list_filter = ('role', 'is_active', 'invited_at')
    search_fields = ('user__username', 'user__email', 'organization__organization_name')
    raw_id_fields = ('user', 'organization', 'invited_by')
    readonly_fields = ('invited_at', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Membership', {
            'fields': ('organization', 'user', 'role', 'is_active')
        }),
        ('Invitation Info', {
            'fields': ('invited_by', 'invited_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Register your models here.
admin.site.register(Organization)
admin.site.register(Employee)