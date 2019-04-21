from datetime import datetime
from django.db import models


# Create your models here.
class Employee(models.Model):

    def __str__(self):
        return self.first_name+" "+self.last_name

    GENDER = (("M", "Male"), ("F", "Female"), ("O", "Other"))
    STATUS = (("S", "Single"), ("M", "Married"), ("D", "Divorced"), ("O", "Other"))
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    address = models.TextField()
    gender = models.CharField(max_length=1, choices=GENDER)
    marital_status = models.CharField(max_length=1, choices=STATUS)
    pan_no = models.CharField(max_length=10)
    aadhar_no = models.CharField(max_length=16)
    position = models.CharField(max_length=50)
    dept = models.CharField(max_length=50)
    join_date = models.DateField(auto_now_add=True)


class Office(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class SalaryRecord (models.Model):
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    base_salary = models.FloatField()
    hra = models.FloatField()
    da = models.FloatField()
    ta = models.FloatField()
    pf = models.FloatField()
    working_days = models.IntegerField()
    leaves = models.IntegerField()
    salary_date = models.DateField(auto_now_add=True)