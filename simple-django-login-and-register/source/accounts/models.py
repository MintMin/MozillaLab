from django.db import models
from django.contrib.auth.models import User

USER_CHOICES = (
   ('Student', 'Student'),
   ('Recruiter', 'Recruiter')
)

class Profile(models.Model): # Child of User
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   user_type = models.CharField(max_length=20)
   #forms.ChoiceField(choices=USER_CHOICES, widget=forms.RadioSelect())


class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
