from django.shortcuts import render
from .models import Career_Fair, Career_Booth
from accounts.models import Student, Recruiter
from django.views.generic import TemplateView, CreateView
from .forms import uni_list, CreateBoothForm
from time import strftime
from dal import autocomplete
from django.contrib import messages
from django.http import HttpResponseRedirect
import time
import datetime
from django.shortcuts import get_object_or_404
from django.forms import ValidationError

class AutocompleteUni(autocomplete.Select2ListView):
    def get_list(self):
        return uni_list()

def getDateRangeFromWeek(p_year,p_week):

    firstdayofweek = datetime.datetime.strptime(f'{p_year}-W{int(p_week )- 1}-1', "%Y-W%W-%w").date()
    lastdayofweek = firstdayofweek + datetime.timedelta(days=6.9)
    return firstdayofweek, lastdayofweek

class CreateBooth(CreateView):
	template_name = 'career_fair/create_booth.html'
	model = Career_Booth
	form_class = CreateBoothForm
	def save(self, *args, **kwargs):
		self.absolute_url = self.get_absolute_url()
		super(event, self).save(*args, **kwargs)
	def form_valid(self, form):
		booth = form.save()
		request = self.request
		booth.recruiter = request.user
		recruiter = Recruiter.objects.filter(user = request.user)[0]
		# Check for career fairs, if none exist, create one
		week_number = booth.date.strftime("%V")
		year = booth.date.year
		firstdate, lastdate =  getDateRangeFromWeek(year,week_number)
		booth.company = recruiter.company
		existing_fairs = Career_Fair.objects.filter(firstdate=firstdate, lastdate = lastdate, university = booth.university)
		if(len(existing_fairs) == 0):
			fair = Career_Fair.objects.create(university = booth.university,
			                     firstdate = firstdate,
			                     lastdate = lastdate)
		else:
			fair = existing_fairs[0]
			existing_booths = Career_Booth.objects.filter(career_fair = fair, company = booth.company)
			if(len(existing_booths) > 0):
				return HttpResponseRedirect('/career_fair/error')
		booth.career_fair = fair
		form.save()
		messages.success(request, ('You have successfully signed up for a booth at a career fair'))
		return HttpResponseRedirect('/career_fair')

def detail(request, event_id):
	career_fair = get_object_or_404(Career_Fair, pk=event_id)
	booths = Career_Booth.objects.filter(career_fair = career_fair)
	return render(request, 'career_fair/view_booths.html', {'event': career_fair, 'booths': booths})

class BoothError(TemplateView):
	template_name = 'career_fair/booth_creation_error.html'

class CareerFairDashboard(TemplateView):
	template_name = 'career_fair/career_fair_dashboard.html'
	def get_context_data(self, **kwargs):
		request = self.request
		context = super(CareerFairDashboard, self).get_context_data(**kwargs)
		if(request.user.is_student):
			student = Student.objects.filter(user = request.user)[0]
			context['career_list'] = Career_Fair.objects.filter(university = student.university).order_by('firstdate')
		elif(request.user.is_recruiter):
			recruiter = Recruiter.objects.filter(user = request.user)[0]
			context['career_list'] = Career_Fair.objects.all().order_by('firstdate')
			# context['joined_fairs'] = Career_Fair.objects.filter()
		return context