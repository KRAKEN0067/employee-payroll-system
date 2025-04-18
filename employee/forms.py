from django import forms
from .models import Employee, Attendance, Bonus, Payroll, Department, Role, Deductions
from datetime import date

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'phone', 'hire_date', 'department', 'role', 'status']
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }


class BonusForm(forms.ModelForm):
    class Meta:
        model = Bonus
        fields = ['employee', 'bonus_amount', 'bonus_date', 'bonus_reason']

class DeductionsForm(forms.ModelForm):
    class Meta:
        model = Deductions
        fields = ['tax','provident_fund','other_deductions','total_deductions']



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

class AttendanceForm(forms.ModelForm):
    date = forms.DateField(
        initial=date.today,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    work_hours = forms.IntegerField(
        initial=0,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Work hours'})
    )
    overtime_hours = forms.IntegerField(
        initial=0,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Overtime hours'})
    )

    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'status', 'work_hours', 'overtime_hours']
