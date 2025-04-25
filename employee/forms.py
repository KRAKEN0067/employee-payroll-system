from django import forms
from .models import Employee, Attendance, Bonus, Payroll, Department, Role, Deductions, SalaryStructure
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
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'bonus_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'bonus_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bonus_reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(BonusForm, self).__init__(*args, **kwargs)
        if not self.initial.get('bonus_date'):
            self.initial['bonus_date'] = date.today()




class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ['employee', 'salary_month', 'payment_status']
        widgets = {
            'salary_month': forms.DateInput(attrs={'type': 'month'})
        }

    def __init__(self, *args, **kwargs):
        super(PayrollForm, self).__init__(*args, **kwargs)
        self.fields['salary_month'].initial = date.today().strftime('%Y-%m')  # "2025-04"


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

class SalaryStructureForm(forms.ModelForm):
    class Meta:
        model = SalaryStructure
        fields = [
            'employee',
            'basic_salary',
            'medical_allowance',
            'travel_allowance',
            'hra'
        ]
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'basic_salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'medical_allowance': forms.NumberInput(attrs={'class': 'form-control'}),
            'travel_allowance': forms.NumberInput(attrs={'class': 'form-control'}),
            'hra': forms.NumberInput(attrs={'class': 'form-control'}),
        }



class DeductionsForm(forms.ModelForm):
    class Meta:
        model = Deductions
        fields = ['employee', 'tax', 'provident_fund', 'other_deductions']
        