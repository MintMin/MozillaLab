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
		fields = ('title', 'Event_type', 'date', 'time', 'summary')
	years_to_display = range(datetime.datetime.now().year,
	datetime.datetime.now().year + 2)
	date = forms.DateField(widget=SelectDateWidget(years=years_to_display))
	# main_recruiter = forms.CharField(label = 'Main Recruiter', max_length=40, required=True)
	time = forms.TimeField(
        widget=SelectTimeWidget()
    )
	# time = forms.TimeField(
 #        widget=SelectTimeWidget(dashed=True, race_time=True)
 #    )
