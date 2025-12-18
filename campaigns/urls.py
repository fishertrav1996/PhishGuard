from django.urls import path
from . import views

app_name = 'campaigns'

urlpatterns = [
    path('track/<uuid:token>/', views.track_click, name='track_click'),
    path('', views.campaign_list, name='campaign_list'),
    path('create/', views.create_campaign, name='create_campaign'),
    path('<uuid:campaign_uuid>/', views.campaign_detail, name='campaign_detail'),
    path('<uuid:campaign_uuid>/send/', views.send_campaign, name='send_campaign'),
]
