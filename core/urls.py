from django.urls import path
from . import views

urlpatterns = [
    path('home', views.get_home_page, name='home'),
    path('about', views.get_about_page, name='about'),
    path('faq', views.get_faq_page, name='FAQ'),
]