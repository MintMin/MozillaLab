from django import forms
from django.forms import ValidationError
from django.conf import settings
from .models import Event
from django.utils import timezone
from django.db.models import Q

from django.forms import ModelForm

from django.db import transaction
from dal import autocomplete

import datetime
from django.forms.widgets import SelectDateWidget
from .widgets import SelectTimeWidget

class CreateEventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ('title', 'date', 'start_time', 'end_time','summary', 'rsvp_capacity')
	years_to_display = range(datetime.datetime.now().year,
	datetime.datetime.now().year + 2)
	date = forms.DateField(
		widget=SelectDateWidget(years=years_to_display),
		initial = datetime.datetime.now(),
	)
	start_time = forms.TimeField(
        widget=SelectTimeWidget(),
		initial = datetime.time(9,00),
    )

	end_time = forms.TimeField(
        widget=SelectTimeWidget(),
		initial = datetime.time(12,00),
    )
	
	rsvp_capacity = forms.IntegerField(label='Maximum Number of Students to Attend')