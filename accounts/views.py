from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import NewUserForm, UserLoginForm

#TODO Finish and test user login functionality
def new_user_view(req):
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
            #TODO Maybe redirect here to success page or login page
            return HttpResponse("User created successfully")


        else:
            messages.error(req, "There were errors in the new user form. Please correct them and try again.")
            return render(req, "accounts/new_user_form.html", {"form": form})

    elif req.method == 'GET':
        form = NewUserForm()
        return render(req, 'accounts/new_user_form.html', {'form': form})
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])
    

def user_login_view(req):
    if req.method == 'POST':
        form = UserLoginForm(req.POST)
        if form.is_valid():
            # Extract cleaned data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate and login if user exists
            current_user = authenticate(username=username, password=password)
            if current_user is not None:
                login(req, current_user)
                #TODO Redirect to a success page or home page
                return HttpResponseRedirect('/home')
                #return HttpResponse("Login successful!")
            else:
                messages.error(req, "Invalid username/password.")
                return render(req, "accounts/login_form.html", {"form": form})
        else:
            messages.error(req, "There were errors in the login form. Please correct them and try again.")
            return render(req, "accounts/login_form.html", {"form": form})
        
    elif req.method == 'GET':
        #TODO If GET request but the user is already authenticated, redirect to home page
        
        form = UserLoginForm()
        return render(req, 'accounts/login_form.html', {'form': form})
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


