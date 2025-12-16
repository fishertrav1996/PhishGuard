from django import forms
from .models import Organization, HEALTHCARE_ORG_TYPES, SUBSCRIPTION_TYPES

class NewOrgForm(forms.ModelForm):
    organization_type = forms.ChoiceField(
        choices=HEALTHCARE_ORG_TYPES,
        label='Organization Type'
    )
    subscription_type = forms.ChoiceField(
        choices=SUBSCRIPTION_TYPES,
        label='Subscription Type'
    )

    class Meta:
        model = Organization
        fields = [
            'organization_name',
            'organization_type',
            'website',
            'street_address_1',
            'street_address_2',
            'city',
            'state_province',
            'postal_code',
            'country',
            'subscription_type'
        ]
        labels = {
            'organization_name': 'Organization Name',
            'organization_type': 'Organization Type',
            'website': 'Website',
            'street_address_1': 'Street Address',
            'street_address_2': 'Street Address 2 (Optional)',
            'city': 'City',
            'state_province': 'State/Province',
            'postal_code': 'Postal Code',
            'country': 'Country',
            'subscription_type': 'Subscription Type'
        }
