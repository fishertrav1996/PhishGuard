from django.urls import path
from . import views

app_name = 'campaigns'

urlpatterns = [
    path('track/<uuid:token>/', views.track_click, name='track_click'),
    path('remediation/<uuid:token>/', views.complete_remediation, name='complete_remediation'),
    path('', views.campaign_list, name='campaign_list'),
    path('create/', views.create_campaign, name='create_campaign'),
    path('<uuid:campaign_uuid>/', views.campaign_detail, name='campaign_detail'),
    path('<uuid:campaign_uuid>/send/', views.send_campaign, name='send_campaign'),
    
    # Compliance Reports
    path('reports/<uuid:org_uuid>/', views.list_compliance_reports, name='list_reports'),
    path('reports/<uuid:org_uuid>/generate/', views.generate_compliance_report, name='generate_report'),
    path('report/<uuid:report_uuid>/download/', views.download_compliance_report, name='download_report'),
    path('report/<uuid:report_uuid>/delete/', views.delete_compliance_report, name='delete_report'),
]
