from django import forms
from .models import Employee, Attendance, Bonus, Payroll, Department, Role
from datetime import date

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'phone', 'hire_date', 'department', 'role', 'status']
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }
class AttendanceForm(forms.ModelForm):
    date = forms.DateField(
        initial=date.today,
        widget=forms.DateInput(attrs={'type':'date'})
    )
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'status', 'work_hours', 'overtime_hours']

class BonusForm(forms.ModelForm):
    class Meta:
        model = Bonus
        fields = ['employee', 'bonus_amount', 'bonus_date', 'bonus_reason']

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ['employee', 'salary_month', 'gross_salary', 'deductions', 'net_salary', 'payment_status']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields ='__all__'

class RoleForm(forms.ModelForm):
    class Meta:
        model =  Role
        fields = '__all__'
