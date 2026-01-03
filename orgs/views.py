from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Organization, Employee, OrganizationMembership
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib import messages
from django.db import IntegrityError

from .forms import NewOrgForm, EmployeeForm, EmployeeCSVUploadForm
from .permissions import require_org_membership, get_user_membership

# Eventually add group permission decorator here to restrict access to owners only
@login_required
def new_org_view(req):
    if req.method == 'POST':

        # Process the form data and create a new organization
        form = NewOrgForm(req.POST)
        if form.is_valid():
            # Create the organization without saving to DB yet
            org = form.save(commit=False)
            
            # Set subscription_is_active based on subscription_type
            org.subscription_is_active = (form.cleaned_data['subscription_type'] == 'PREMIUM')
            
            # Save org to DB
            org.save()
            
            # Create OWNER membership for the creator
            OrganizationMembership.objects.create(
                organization=org,
                user=req.user,
                role='OWNER',
                is_active=True
            )

            messages.success(req, "Organization created successfully.")
            return HttpResponseRedirect('/home')
        else:
            messages.error(req, "There were errors in the new org form. Please correct them and try again.")
            return render(req, "orgs/new_org_form.html", {"form": form})
        
    elif req.method == 'GET':
        # Render the form for creating a new organization
        form = NewOrgForm()
        return render(req, 'orgs/new_org_form.html', {'form': form})
    else:
        # Handle other HTTP methods
        return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
@require_org_membership('OWNER', 'ADMIN')
def add_employee_view(req, org_uuid):
    """View for adding a single employee to an organization"""
    # org and org_membership added by decorator
    org = req.organization
    
    if req.method == 'POST':
        form = EmployeeForm(req.POST)
        if form.is_valid():
            try:
                employee = form.save(commit=False)
                employee.organization = org
                employee.save()
                messages.success(req, f"Employee {employee.first_name} {employee.last_name} added successfully.")
                return HttpResponseRedirect(f'/orgs/{org.uuid}/employees/')
            except IntegrityError:
                messages.error(req, "An employee with this email already exists.")
                return render(req, "orgs/add_employee.html", {"form": form, "org": org})
        else:
            messages.error(req, "Please correct the errors below.")
            return render(req, "orgs/add_employee.html", {"form": form, "org": org})
    
    elif req.method == 'GET':
        form = EmployeeForm()
        return render(req, 'orgs/add_employee.html', {'form': form, 'org': org})
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
@require_org_membership('OWNER', 'ADMIN')
def upload_employees_csv_view(req, org_uuid):
    """View for uploading multiple employees via CSV"""
    # org and org_membership added by decorator
    org = req.organization
    
    if req.method == 'POST':
        form = EmployeeCSVUploadForm(req.POST, req.FILES)
        if form.is_valid():
            employees, errors = form.parse_csv(org)
            
            if errors:
                # Show errors to user
                for error in errors:
                    messages.error(req, error)
                return render(req, "orgs/upload_employees_csv.html", {"form": form, "org": org})
            
            # Save all employees
            saved_count = 0
            for employee in employees:
                try:
                    employee.save()
                    saved_count += 1
                except IntegrityError:
                    messages.warning(req, f"Skipped {employee.email} - email already exists.")
            
            messages.success(req, f"Successfully added {saved_count} employee(s).")
            return HttpResponseRedirect(f'/orgs/{org.uuid}/employees/')
        else:
            messages.error(req, "Please correct the errors below.")
            return render(req, "orgs/upload_employees_csv.html", {"form": form, "org": org})
    
    elif req.method == 'GET':
        form = EmployeeCSVUploadForm()
        return render(req, 'orgs/upload_employees_csv.html', {'form': form, 'org': org})
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
@require_org_membership()  # All members can view employee list
def list_employees_view(req, org_uuid):
    """View for listing all employees in an organization"""
    org = req.organization
    
    employees = org.employees.all().order_by('last_name', 'first_name')
    
    return render(req, 'orgs/list_employees.html', {
        'org': org,
        'employees': employees,
        'user_membership': req.org_membership,
    })


@login_required
@require_org_membership('OWNER', 'ADMIN')
def delete_employee_view(req, org_uuid, employee_id):
    """View for deleting an employee from an organization"""
    org = req.organization
    employee = get_object_or_404(Employee, id=employee_id, organization=org)
    
    if req.method == 'DELETE':
        employee_name = f"{employee.first_name} {employee.last_name}"
        employee.delete()
        messages.success(req, f"Employee {employee_name} has been deleted.")
        
        # For HTMX requests, trigger a page reload
        response = HttpResponse(status=200)
        response['HX-Redirect'] = f'/orgs/{org.uuid}/employees/'
        return response
    else:
        return HttpResponseNotAllowed(['DELETE'])
