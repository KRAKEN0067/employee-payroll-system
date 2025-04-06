from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import EmployeeForm, AttendanceForm, BonusForm, PayrollForm, DepartmentForm, RoleForm
from .models import *
def home(request):
    return render(request,'home.html')

def manage(request):
    return render(request, 'manage/manage.html')

def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'service.html')

def contacts(request):
    return render(request, 'contacts.html')


def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'manage/employee_list.html',{'employees':employees})



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
    form = None
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('add_role')
    else:
        form = RoleForm()
    
    return render(request, 'manage/add_role.html', {'form':form})

def add_department(request):
    form = None
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_department')
    else:
        form = DepartmentForm()

    return render(request, 'manage/add_department.html', {'form': form})

def mark_attendance(request):
    form = None
    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AttendanceForm()

    return render(request, 'manage/mark_attendance.html', {'form': form})

def add_bonus(request):
    form = None
    if request.method == "POST":
        form = BonusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BonusForm()

    return render(request, 'manage/add_bonus.html', {'form': form})

def process_payroll(request):
    form = None
    if request.method == "POST":
        form = PayrollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PayrollForm()

    return render(request, 'manage/process_payroll.html', {'form': form})

def payroll_info(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    payrolls = Payroll.objects.filter(employee=employee).order_by('-salary_month')
    return render(request, 'manage/payroll_info.html', {'employee':employee, 'payrolls':payrolls})