from django.urls import path
from . import views

urlpatterns = [
    path('new', views.new_org_view, name='new_org'),
    path('<uuid:org_uuid>/employees/', views.list_employees_view, name='list_employees'),
    path('<uuid:org_uuid>/employees/add/', views.add_employee_view, name='add_employee'),
    path('<uuid:org_uuid>/employees/upload/', views.upload_employees_csv_view, name='upload_employees_csv'),
    path('<uuid:org_uuid>/employees/<int:employee_id>/delete/', views.delete_employee_view, name='delete_employee'),
]