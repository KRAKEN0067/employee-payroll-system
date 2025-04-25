from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import EmployeeForm, AttendanceForm, BonusForm, PayrollForm, DepartmentForm, RoleForm, DeductionsForm
from .models import *
from django.db.models import Q,Sum,Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import calendar
from datetime import datetime, date
import csv

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def home(request):
    return render(request,'home.html')

def manage(request):
    return render(request, 'manage/manage.html')




def employee_list(request):
    query = request.GET.get('q', '')
    department = request.GET.get('department')
    role = request.GET.get('role')
    status = request.GET.get('status')

    employees = Employee.objects.all()

    if query:
        employees = employees.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query) |
            Q(department__department_name__icontains=query) |
            Q(role__role_name__icontains=query)
        )

    if department:
        try:
            employees = employees.filter(department__pk=int(department))
        except ValueError:
            pass  # silently ignore invalid filter

    if role:
        try:
            employees = employees.filter(role__pk=int(role))
        except ValueError:
            pass

    if status:
        employees = employees.filter(status=status)

    departments = Department.objects.all()
    roles = Role.objects.all()

    context = {
        'employees': employees,
        'departments': departments,
        'roles': roles,
    }

    return render(request, 'manage/employee_list.html', context)



def edit_employee(request,employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)

    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'manage/add_employee.html', {'form':form , 'employee': employee})

def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    
    if request.method == "POST":
        employee.delete()
        return redirect('employee_list')
    return render(request, 'manage/delete_employee.html', {'employee':employee})

def add_employee(request):
    form = None
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_employee')
    else:
        form = EmployeeForm()

    return render(request, 'manage/add_employee.html', {'form': form})

def add_role(request):
    roles = Role.objects.all()
    
    if request.method == "POST":
        form = RoleForm(request.POST)  # ✅ initialize the form with POST data
        if form.is_valid():
            form.save()
            return redirect('add_role')
    else:
        form = RoleForm()  # ✅ initialize an empty form for GET requests
    
    return render(request, 'manage/add_role.html', {'form': form, 'roles': roles})

def add_department(request):
    form = None
    departments = Department.objects.all()
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_department')
    else:
        form = DepartmentForm()

    return render(request, 'manage/add_department.html', {'form': form, 'departments':departments})

def mark_attendance(request):
    form = None
    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mark_attendance')
    else:
        form = AttendanceForm()

    return render(request, 'manage/mark_attendance.html', {'form': form})

def add_bonus(request):
    form = None
    if request.method == "POST":
        form = BonusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_bonus')
    else:
        form = BonusForm()

    return render(request, 'manage/add_bonus.html', {'form': form})


def process_payroll(request):
    form = None
    if request.method == "POST":
        form = PayrollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('process_payroll')
    else:
        form = PayrollForm()

    return render(request, 'manage/process_payroll.html', {'form': form})

def payroll_info(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    payrolls = Payroll.objects.filter(employee=employee)
    salary_structure = SalaryStructure.objects.filter(employee=employee).first()
    deductions = Deductions.objects.filter(employee=employee).first()
    bonuses = Bonus.objects.filter(employee=employee)

    return render(request, 'manage/payroll_info.html', {
        'employee': employee,
        'payrolls': payrolls,
        'salary_structure': salary_structure,
        'deductions': deductions,
        'bonuses': bonuses,
    })




def employee_stats_view(request):
     employees = Employee.objects.all()
     employee_data = []
 
     attendance_chart_data = []
     salary_chart_data = []
     bonus_chart_data = []
 
     for emp in employees:
         attendance = Attendance.objects.filter(employee=emp)
         attendance_summary = {
             'present': attendance.filter(status='Present').count(),
             'absent': attendance.filter(status='Absent').count(),
             'on_leave': attendance.filter(status='On Leave').count(),
         }
 
         latest_payroll = Payroll.objects.filter(employee=emp).order_by('-payroll_id').first()
         net_salary = latest_payroll.net_salary if latest_payroll else 0
         total_bonus = Bonus.objects.filter(employee=emp).aggregate(total=Sum('bonus_amount'))['total'] or 0
 
         employee_data.append({
             'employee': emp,
             'attendance_summary': attendance_summary,
             'net_salary': net_salary,
             'latest_pay_month': latest_payroll.salary_month if latest_payroll else 'N/A',
             'bonus_total': total_bonus,
         })
 
         # Graph data
         attendance_chart_data.append({
             'name': f'{emp.first_name} {emp.last_name}',
             'present': attendance_summary['present'],
             'absent': attendance_summary['absent'],
             'on_leave': attendance_summary['on_leave'],
         })
         salary_chart_data.append({
             'name': f'{emp.first_name} {emp.last_name}',
             'salary': float(net_salary),
         })
         bonus_chart_data.append({
             'name': f'{emp.first_name} {emp.last_name}',
             'bonus': float(total_bonus),
         })
 
     # Sort salary chart to get top 5 earners
     top_5_salaries = sorted(salary_chart_data, key=lambda x: x['salary'], reverse=True)[:5]
 
     context = {
         'employee_data': employee_data,
         'attendance_chart_data': attendance_chart_data,
         'top_5_salaries': top_5_salaries,
         'bonus_chart_data': bonus_chart_data,
     }
 
     return render(request, 'manage/employee_stats.html', context)

def individual_stats(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    attendance_records = Attendance.objects.filter(employee=employee)
    payrolls = Payroll.objects.filter(employee=employee)
    bonuses = Bonus.objects.filter(employee=employee)
    salary = SalaryStructure.objects.filter(employee=employee).first()
    deductions = Deductions.objects.filter(employee=employee).first()

    present_days = attendance_records.filter(status='Present').count()
    absent_days = attendance_records.filter(status='Absent').count()
    leave_days = attendance_records.filter(status='On Leave').count()
    total_work_hours = sum(record.work_hours for record in attendance_records)
    total_overtime = sum(record.overtime_hours for record in attendance_records)

    attendance_data = {
    'Present': present_days,
    'Absent': absent_days,
    'On_Leave': leave_days,
}

    context = {
        'employee': employee,
        'attendance_data':attendance_data,
        'present_days': present_days,
        'absent_days': absent_days,
        'leave_days': leave_days,
        'total_work_hours': total_work_hours,
        'total_overtime': total_overtime,
        'payrolls': payrolls,
        'bonuses': bonuses,
        'salary': salary,
        'deductions': deductions,
    }
    return render(request, 'manage/individual_stats.html', context)

def export_employees_csv(request):
    # Create the HttpResponse object with CSV headers
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employee_list.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['Employee ID', 'Name', 'Email', 'Phone', 'Department', 'Role', 'Status'])

    # Filter employees based on query parameters
    query = request.GET.get('q', '')
    department = request.GET.get('department')
    role = request.GET.get('role')
    status = request.GET.get('status')

    employees = Employee.objects.all()

    # Apply search query
    if query:
        employees = employees.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query) |
            Q(department_department_name_icontains=query) |
            Q(role_role_name_icontains=query)
        )

    # Apply department filter
    if department:
        try:
            employees = employees.filter(department__pk=int(department))
        except ValueError:
            pass  # Ignore invalid department filter

    # Apply role filter
    if role:
        try:
            employees = employees.filter(role__pk=int(role))
        except ValueError:
            pass  # Ignore invalid role filter

    # Apply status filter
    if status:
        employees = employees.filter(status=status)

    # Write employee data rows
    for employee in employees:
        writer.writerow([
            employee.employee_id,
            f"{employee.first_name} {employee.last_name}",
            employee.email,
            employee.phone,
            employee.department.department_name if employee.department else '',
            employee.role.role_name if employee.role else '',
            employee.status
        ])

    return response