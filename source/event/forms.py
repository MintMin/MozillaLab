from django import forms
from django.forms import ValidationError
from django.conf import settings
from .models import Event
from django.utils import timezone
from django.db.models import Q

from django.forms import ModelForm

from django.db import transaction

class CreateEventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = '__all__'