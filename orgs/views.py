from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def hello_world_view(req):
    return HttpResponse('Hello There!')