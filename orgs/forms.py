from django import forms

class NewOrgForm(forms.Form):
    organization_name = forms.CharField(label='Organization Name', max_length=100)
    #TODO current user should be set as owner
    owner = forms.CharField(label='Owner', max_length=100)
    organization_type = forms.CharField(label='Organization Type', max_length=100)
    website = forms.URLField(label='Website', required=False)
    street_address = forms.CharField(label='Street Address', max_length=255)
    city = forms.CharField(label='City', max_length=100)
    state = forms.CharField(label='State', max_length=100)
    zip_code = forms.CharField(label='Zip Code', max_length=20)
    country = forms.CharField(label='Country', max_length=100)
