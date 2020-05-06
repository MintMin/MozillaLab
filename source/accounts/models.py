from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

USER_CHOICES = (
   ('Student', 'Student'),
   ('Recruiter', 'Recruiter')
)


class CustomUser(AbstractUser):
	is_student = models.BooleanField('student status', default=False)
	is_recruiter = models.BooleanField('recruiter status', default=False)

class Profile(models.Model): # Child of User
   user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
   user_type = models.CharField(max_length=20)
   #forms.ChoiceField(choices=USER_CHOICES, widget=forms.RadioSelect())

class Activation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    major = models.CharField(max_length=100)