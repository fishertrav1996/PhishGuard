from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Organization, Employee
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib import messages
from django.db import IntegrityError

from .forms import NewOrgForm, EmployeeForm, EmployeeCSVUploadForm

# Eventually add group permission decorator here to restrict access to owners only
@login_required
def new_org_view(req):
    if req.method == 'POST':

        # Process the form data and create a new organization
        form = NewOrgForm(req.POST)
        if form.is_valid():
            # Create the organization without saving to DB yet
            org = form.save(commit=False)
            
            # Set the owner to the current user
            org.owner = req.user
            
            # Set subscription_is_active based on subscription_type
            org.subscription_is_active = (form.cleaned_data['subscription_type'] == 'PREMIUM')
            
            # Save org to DB and return success
            org.save()

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
def add_employee_view(req, org_id):
    """View for adding a single employee to an organization"""
    # Get the organization and verify ownership
    org = get_object_or_404(Organization, id=org_id)
    
    if org.owner != req.user:
        messages.error(req, "You don't have permission to add employees to this organization.")
        return HttpResponseRedirect('/home')
    
    if req.method == 'POST':
        form = EmployeeForm(req.POST)
        if form.is_valid():
            try:
                employee = form.save(commit=False)
                employee.organization = org
                employee.save()
                messages.success(req, f"Employee {employee.first_name} {employee.last_name} added successfully.")
                return HttpResponseRedirect(f'/orgs/{org_id}/employees/')
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
def upload_employees_csv_view(req, org_id):
    """View for uploading multiple employees via CSV"""
    # Get the organization and verify ownership
    org = get_object_or_404(Organization, id=org_id)
    
    if org.owner != req.user:
        messages.error(req, "You don't have permission to add employees to this organization.")
        return HttpResponseRedirect('/home')
    
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
            return HttpResponseRedirect(f'/orgs/{org_id}/employees/')
        else:
            messages.error(req, "Please correct the errors below.")
            return render(req, "orgs/upload_employees_csv.html", {"form": form, "org": org})
    
    elif req.method == 'GET':
        form = EmployeeCSVUploadForm()
        return render(req, 'orgs/upload_employees_csv.html', {'form': form, 'org': org})
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
def list_employees_view(req, org_id):
    """View for listing all employees in an organization"""
    org = get_object_or_404(Organization, id=org_id)
    
    if org.owner != req.user:
        messages.error(req, "You don't have permission to view this organization's employees.")
        return HttpResponseRedirect('/home')
    
    employees = org.employees.all().order_by('last_name', 'first_name')
    
    return render(req, 'orgs/list_employees.html', {'org': org, 'employees': employees})
