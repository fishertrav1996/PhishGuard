from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def hello_world_view(req):
    return HttpResponse('Hello There!')

def hello_html_view(req):
    return render(req, 'orgs/home.html')

def hello_path_view(req, name):
    return HttpResponse(f'Hello, {name}!')

def hello_query_view(req):
    name = req.GET.get('name')
    return HttpResponse(f'Hello, {name}!')