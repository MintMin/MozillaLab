from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Recruiter, Student

# Register your models here.
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Recruiter)
admin.site.register(Student)