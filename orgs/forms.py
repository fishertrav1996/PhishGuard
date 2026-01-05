from django import forms
from .models import Organization, Employee, HEALTHCARE_ORG_TYPES, SUBSCRIPTION_TIER_CHOICES, US_STATES
import csv
import io

class NewOrgForm(forms.ModelForm):
    organization_type = forms.ChoiceField(
        choices=HEALTHCARE_ORG_TYPES,
        label='Organization Type'
    )
    state_province = forms.ChoiceField(
        choices=US_STATES,
        label='State'
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
        ]
        labels = {
            'organization_name': 'Organization Name',
            'organization_type': 'Organization Type',
            'website': 'Website',
            'street_address_1': 'Street Address',
            'street_address_2': 'Street Address 2 (Optional)',
            'city': 'City',
            'state_province': 'State',
            'postal_code': 'Postal Code',
            'country': 'Country',
        }


class EmployeeForm(forms.ModelForm):
    """Form for adding a single employee"""
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'role', 'position']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'role': 'Role',
            'position': 'Position/Title'
        }


class EmployeeCSVUploadForm(forms.Form):
    """Form for uploading CSV file with multiple employees"""
    csv_file = forms.FileField(
        label='Upload CSV File',
        help_text='CSV should have headers: first_name, last_name, email, role, position'
    )
    
    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        
        # Check file extension
        if not csv_file.name.endswith('.csv'):
            raise forms.ValidationError('File must be a CSV file.')
        
        # Check file size (limit to 5MB)
        if csv_file.size > 5 * 1024 * 1024:
            raise forms.ValidationError('File size must be under 5MB.')
        
        return csv_file
    
    def parse_csv(self, organization):
        """Parse CSV and return list of Employee objects and errors"""
        csv_file = self.cleaned_data['csv_file']
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)
        
        employees = []
        errors = []
        valid_roles = [choice[0] for choice in Employee._meta.get_field('role').choices]
        
        for row_num, row in enumerate(reader, start=2):  # Start at 2 (1 is header)
            try:
                # Validate required fields
                required_fields = ['first_name', 'last_name', 'email']
                missing_fields = [field for field in required_fields if not row.get(field, '').strip()]
                
                if missing_fields:
                    errors.append(f"Row {row_num}: Missing required fields: {', '.join(missing_fields)}")
                    continue
                
                # Validate role if provided
                role = row.get('role', 'STAFF').strip().upper()
                if role and role not in valid_roles:
                    errors.append(f"Row {row_num}: Invalid role '{role}'. Must be one of: {', '.join(valid_roles)}")
                    continue
                
                # Create employee object (don't save yet)
                employee = Employee(
                    organization=organization,
                    first_name=row['first_name'].strip(),
                    last_name=row['last_name'].strip(),
                    email=row['email'].strip().lower(),
                    role=role or 'STAFF',
                    position=row.get('position', '').strip()
                )
                
                employees.append(employee)
                
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
        
        return employees, errors
