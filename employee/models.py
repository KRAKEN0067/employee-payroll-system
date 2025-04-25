from django.db import models


class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    department_code = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.department_name


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.role_name


class Employee(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    hire_date = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class SalaryStructure(models.Model):
    salary_id = models.AutoField(primary_key=True)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    travel_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Auto-calculate gross salary before saving
        self.gross_salary = (
            self.basic_salary +
            self.medical_allowance +
            self.travel_allowance +
            self.hra
        )
        super(SalaryStructure, self).save(*args, **kwargs)

    def __str__(self):
        return f"Salary ID: {self.salary_id} - Employee: {self.employee.first_name}"


class Deductions(models.Model):
    deduction_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    provident_fund = models.DecimalField(max_digits=10, decimal_places=2)
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Deduction ID: {self.deduction_id} - Employee: {self.employee.employee_id}"


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('On Leave', 'On Leave')
    ]
    attendance_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    work_hours = models.IntegerField()
    overtime_hours = models.IntegerField()

    def __str__(self):
        return f"Attendance ID: {self.attendance_id} - Employee: {self.employee.first_name}"

class Payroll(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]
    payroll_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary_month = models.CharField(max_length=20)  # Can be 'March 2025'
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES)
    

    def __str__(self):
        return f"Payroll ID: {self.payroll_id} - Employee: {self.employee.first_name}"


class Bonus(models.Model):
    bonus_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    bonus_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bonus_date = models.DateField()
    bonus_reason = models.TextField()

    def __str__(self):
        return f"Bonus ID: {self.bonus_id} - Employee: {self.employee.first_name}"
