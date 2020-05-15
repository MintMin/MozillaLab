from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
	is_student = models.BooleanField('student status', default=False)
	is_recruiter = models.BooleanField('recruiter status', default=False)

class Profile(models.Model): # Child of User
   user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
   user_type = models.CharField(max_length=20)

class Activation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)

class Student(models.Model): #to be merged with StudentProfile
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    school = models.CharField(max_length = 100)
    major = models.CharField(max_length=100)

class Recruiter(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True,null=True)
    company = models.CharField(max_length = 100)

class StudentProfile(models.Model): #to be merged with Student
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE) #might need to change user..
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    university = models.CharField(max_length=100) #change to autocomplete
    major = models.CharField(max_length=100) #change to autocomplete
    grad_date = models.DateField()
    career_interest = models.CharField(max_length=100) #change to autocomplete