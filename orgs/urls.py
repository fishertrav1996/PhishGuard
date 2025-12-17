from django.urls import path
from . import views

urlpatterns = [
    path('new', views.new_org_view, name='new_org'),
    path('<int:org_id>/employees/', views.list_employees_view, name='list_employees'),
    path('<int:org_id>/employees/add/', views.add_employee_view, name='add_employee'),
    path('<int:org_id>/employees/upload/', views.upload_employees_csv_view, name='upload_employees_csv'),
]