from django.urls import path
from . import views

app_name = 'campaigns'

urlpatterns = [
    path('track/<uuid:token>/', views.track_click, name='track_click'),
    path('', views.campaign_list, name='campaign_list'),
    path('create/', views.create_campaign, name='create_campaign'),
    path('<int:campaign_id>/', views.campaign_detail, name='campaign_detail'),
    path('<int:campaign_id>/send/', views.send_campaign, name='send_campaign'),
]
