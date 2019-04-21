from django.contrib import admin

# Register your models here.
from .models import Employee, Office, SalaryRecord
admin.site.register(Employee)
admin.site.register(Office)
admin.site.register(SalaryRecord)
