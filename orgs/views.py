from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Organization
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib import messages

from .forms import NewOrgForm

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
