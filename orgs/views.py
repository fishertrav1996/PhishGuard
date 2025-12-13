from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Organization
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib import messages

from .forms import NewOrgForm

#TODO Updates fields and test
# Eventually add group permission decorator here to restrict access to owners only
@login_required
def new_org_view(req):
    if req.method == 'POST':

        # Process the form data and create a new organization
        form = NewOrgForm(req.POST)
        if form.is_valid():
            # Extract cleaned data and create the organization
            org_name = form.cleaned_data['organization_name']
            owner = req.user
            org_type = form.cleaned_data['organization_type']
            website = form.cleaned_data['website']
            street_address = form.cleaned_data['street_address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip_code = form.cleaned_data['zip_code']
            country = form.cleaned_data['country']

            org = Organization.objects.create(
                organization_name=org_name,
                owner=owner,
                organization_type=org_type,
                website=website,
                street_address_1=street_address,
                city=city,
                state_province=state,
                postal_code=zip_code,
                country=country
            )

            # Save org to DB and return success
            org.save()

            messages.success(req, "Organization created successfully.")
            return HttpResponseRedirect('/home')
        else:
            messages.error(req, "There were errors in the new user form. Please correct them and try again.")
            return render(req, "orgs/new_org_form.html", {"form": form})
        
    elif req.method == 'GET':
        # Render the form for creating a new organization
        form = NewOrgForm()
        return render(req, 'orgs/new_org_form.html', {'form': form})
    else:
        # Handle other HTTP methods
        return HttpResponseNotAllowed(['GET', 'POST'])


def hello_world_view(req):
    return HttpResponse('Hello There!')

def hello_html_view(req):
    return render(req, 'orgs/home.html')

def hello_path_view(req, name):
    return HttpResponse(f'Hello, {name}!')

def hello_query_view(req):
    name = req.GET.get('name')
    return HttpResponse(f'Hello, {name}!')