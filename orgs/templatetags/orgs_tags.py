from django import template
from orgs.models import Organization

register = template.Library()


@register.simple_tag
def get_user_organization(user):
    """
    Get the first organization the user is a member of.
    Returns the user's first organization based on membership.
    """
    try:
        return Organization.objects.filter(
            memberships__user=user,
            memberships__is_active=True
        ).first()
    except Organization.DoesNotExist:
        return None
