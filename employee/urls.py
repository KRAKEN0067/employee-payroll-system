from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('add_employee/', add_employee, name='add_employee'),
    path('add_deparment/', add_department, name='add_department'),
    path('add_role/', add_role, name='add_role'),
    path('mark_attendance/', mark_attendance, name='mark_attendance'),
    path('add_bonus/', add_bonus, name='add_bonus'),
    path('process_payroll', process_payroll, name='process_payroll'),
    path('payroll_info/<int:employee_id>', payroll_info, name='payroll_info'),

    path('employee_list/', employee_list, name='employee_list'),
    path('edit_employee/<int:employee_id>/', edit_employee, name='edit_employee'),
    path('delete_employee/<int:employee_id>/', delete_employee, name='delete_employee'),

    path('manage/', manage, name='manage'),
    path('about/', about, name='about'),
    path('service/', service, name='service'),
    path('contacts/', contacts, name='contacts'),

]
