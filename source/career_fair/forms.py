from django import forms
from django.forms import ValidationError
from django.conf import settings
from .models import Career_Booth
from django.utils import timezone
from django.db.models import Q

from django.forms import ModelForm

from dal import autocomplete

import datetime
from django.forms.widgets import SelectDateWidget
from event.widgets import SelectTimeWidget

def uni_list():
    return settings.UNIV_LIST

class CreateBoothForm(forms.ModelForm):
	class Meta:
		model = Career_Booth
		fields = ('interview_duration', 'rest_duration','date', 'time_start', 'time_end', 'university')
	years_to_display = range(datetime.datetime.now().year,
	datetime.datetime.now().year + 2)
	date = forms.DateField(widget=SelectDateWidget(years=years_to_display), required = True)
	time_start = forms.TimeField(
		widget=SelectTimeWidget(),
		required = True
		)
	time_end = forms.TimeField(
		widget=SelectTimeWidget(),
		required = True
		)
	university = autocomplete.Select2ListCreateChoiceField(
		choice_list=uni_list(),
		required=True,
		widget=autocomplete.ListSelect2(url='accounts:uni-autocomplete')
		#initial = self.user.university
		)
	# booth_name = forms.CharField(max_length=100)
	# @property
 #    def booth_check(self):
 #    	request = self.request
	# 	recruiter = request.user
	# 	recruiter_object = Recruiter.objects.filter(user = request.user)[0]
	# 	# Check for career fairs, if none exist, create one
	# 	week_number = booth.date.strftime("%V")
	# 	year = booth.date.year
	# 	firstdate, lastdate =  getDateRangeFromWeek(year,week_number)
	# 	booth.company = recruiter.company
 #        return ['email_or_username', 'password']
