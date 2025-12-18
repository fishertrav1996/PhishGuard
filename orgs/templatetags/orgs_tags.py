from django import template
from orgs.models import Organization

register = template.Library()


@register.simple_tag
def get_user_organization(user):
    """
    Get the first organization owned by the user.
    TODO: Update this when implementing multi-org support per user.
    """
    try:
        return Organization.objects.filter(owner=user).first()
    except Organization.DoesNotExist:
        return None
