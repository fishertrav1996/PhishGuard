from django.urls import path
from . import views

urlpatterns = [
    path('hello', views.hello_world_view, name='hello world'),
    path('hello/<str:name>', views.hello_path_view, name='hello name'),
    path('hello_query', views.hello_query_view, name='hello query'),
]