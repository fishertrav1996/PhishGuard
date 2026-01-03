"""
Context processors for adding organization membership data to templates.
"""
from .permissions import get_user_organizations


def user_organizations(request):
    """
    Add user's organizations to template context.
    Makes 'user_organizations' available in all templates.
    """
    if request.user.is_authenticated:
        return {
            'user_organizations': get_user_organizations(request.user)
        }
    return {
        'user_organizations': []
    }
