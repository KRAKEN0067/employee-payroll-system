from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home, name='home'),
    path('add_employee/', add_employee, name='add_employee'),
    path('employee-stats/', employee_stats_view, name='employee_stats'),
    path('add_deparment/', add_department, name='add_department'),
    path('add_role/', add_role, name='add_role'),
    path('mark_attendance/', mark_attendance, name='mark_attendance'),
    path('add_bonus/', add_bonus, name='add_bonus'),
    path('add_salary_structure/', add_salary_structure, name='add_salary_structure'),
    path('add_deductions/', add_deductions,name='add_deductions'),
    path('process_payroll', process_payroll, name='process_payroll'),
    path('payroll_info/<int:employee_id>', payroll_info, name='payroll_info'),
    path('employee_list/', employee_list, name='employee_list'),
    path('export-employees/', export_employees_csv, name='export_employees_csv'),
    path('edit_employee/<int:employee_id>/', edit_employee, name='edit_employee'),
    path('individual_stats/<int:employee_id>/', individual_stats, name='individual_stats'),
    path('delete_employee/<int:employee_id>/', delete_employee, name='delete_employee'),
    path('manage/', manage, name='manage'),

    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register, name='register'),
    
]
