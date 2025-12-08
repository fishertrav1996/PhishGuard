from django.urls import path
from . import views

urlpatterns = [
    path('new-user', views.get_new_user_form, name='new-user-form'),
    path('register', views.post_new_user, name='post_new_user')
]