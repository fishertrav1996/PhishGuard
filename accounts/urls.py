from django.urls import path
from . import views

urlpatterns = [
    path('new-user', views.new_user_view, name='new_user'),
    path('login', views.user_login_view, name='user_login'),
    path('logout', views.user_logout_view, name='user_logout'),
]