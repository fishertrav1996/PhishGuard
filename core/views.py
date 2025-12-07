from django.shortcuts import render

def get_home_page(req):
    return render(req, 'core/home.html')

def get_about_page(req):
    return render(req, 'core/about.html')

def get_faq_page(req):
    return render(req, 'core/faq.html')