from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User
from .forms import NewUserForm

# Create your views here.
def post_new_user(req):
    if req.method == 'POST':
        # Process the form data and create a new user
        form = NewUserForm(req.POST)
        if form.is_valid():
            # Extract cleaned data
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create user object
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Save the user to the database
            user.save()
            return HttpResponse("User created successfully")


        else:
            return render(req, "accounts/new_user.html", {"form": form})

    else:
        return HttpResponseNotAllowed(['POST'])
    
def get_new_user_form(req):

    form = NewUserForm()

    if req.method == 'GET':
        return render(req, 'accounts/new_user_form.html', {'form': form})
    else:
        return HttpResponseNotAllowed(['GET'])
