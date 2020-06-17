from django.shortcuts import render
from .models import Career_Fair, Career_Booth, Dictionary_Booth, KeyVal
from event.models import Event
from accounts.models import Student, Recruiter
from django.views.generic import TemplateView, CreateView
from .forms import uni_list, CreateBoothForm
from time import strftime
from dal import autocomplete
from django.contrib import messages
from django.http import HttpResponseRedirect
import time
import datetime
from django.shortcuts import get_object_or_404, get_list_or_404
from django.forms import ValidationError
from zoomus import ZoomClient
from datetime import timedelta
from django.utils import timezone

def available(request, slot_id):
	new_slot = KeyVal.objects.filter(pk = slot_id)[0]
	user = request.user
	date = new_slot.container.career_booth.date
	# First check conflicts with career fair
	current_slots = KeyVal.objects.filter(value = user)
	print(current_slots)
	for keyval in current_slots:
		print(keyval.container)
		if(keyval.container.career_booth.date == date):
			# Check the time
			time_to_add = datetime.datetime.strptime(new_slot.key, '%H:%M')
			start_seconds_to_add = time_to_add.hour * 3600 + time_to_add.minute * 60
			duration_to_add = (1 + new_slot.container.career_booth.interview_duration) * 60
			total_add = start_seconds_to_add + duration_to_add
			time_pot_conflict = datetime.datetime.strptime(keyval.key, '%H:%M')
			start_seconds_pot_conflict = time_pot_conflict.hour * 3600 + time_pot_conflict.minute * 60
			duration_pot_conflict = (1 + keyval.container.career_booth.interview_duration) * 60
			total_conflict = start_seconds_pot_conflict + duration_pot_conflict
			# First case is if our new event starts during the potential conflicted event
			# Second case is if our new event ends during the potential conflicted event
			if((start_seconds_to_add >= start_seconds_pot_conflict and 
				start_seconds_to_add <= total_conflict) or
				(total_add >= start_seconds_pot_conflict and total_add <= total_conflict)):
				return False
	# Next, check conflicts with infosessions
	current_infosessions = Event.objects.filter(rsvp_list__in = [user], date = date)
	for infosession in current_infosessions:
		# Check the time
		new_start = datetime.datetime.strptime(new_slot.key, '%H:%M')
		new_start_seconds = new_start.hour * 3600 + new_start.minute * 60
		duration_to_add = (1 + new_slot.container.career_booth.interview_duration) * 60
		new_end_seconds = new_start_seconds + duration_to_add

		old_start_seconds = infosession.start_time.hour * 3600 + infosession.start_time.minute * 60
		old_end_seconds = infosession.end_time.hour * 3600 + infosession.end_time.minute * 60
		# First case is if our new event starts during the potential conflicted event
		# Second case is if our new event ends during the potential conflicted event
		if((new_start_seconds >= old_start_seconds and 
			new_start_seconds <= old_end_seconds) or
			(new_end_seconds >= old_start_seconds and new_end_seconds <= old_end_seconds)):
			return False
	return True

def recruiter_available(request, booth):
	new_booth = booth
	recruiter = request.user
	date = new_booth.date
	new_start_time = new_booth.time_start
	new_end_time = new_booth.time_end
	# First check conflicts with booths
	current_booths = Career_Booth.objects.filter(recruiter = recruiter, date = date)
	for booth in current_booths:
		# Check the time
		# new_start = datetime.datetime.strptime(new_start_time, '%H:%M')
		new_start_seconds = new_start_time.hour * 3600 + new_start_time.minute * 60
		# new_end = datetime.datetime.strptime(new_end_time, '%H:%M')
		new_end_seconds = new_end_time.hour * 3600 + new_end_time.minute * 60

		# old_start = datetime.datetime.strptime(booth.time_start, '%H:%M')
		old_start_seconds = booth.time_start.hour * 3600 + booth.time_start.minute * 60
		# old_end = datetime.datetime.strptime(booth.time_end, '%H:%M')
		old_end_seconds = booth.time_end.hour * 3600 + booth.time_end.minute * 60
		# First case is if our new event starts during the potential conflicted event
		# Second case is if our new event ends during the potential conflicted event
		if((new_start_seconds >= old_start_seconds and 
			new_start_seconds <= old_end_seconds) or
			(new_end_seconds >= old_start_seconds and new_end_seconds <= old_end_seconds)):
			return False
	# Next, check conflicts with infosessions
	current_infosessions = Event.objects.filter(main_recruiter = recruiter, date = date)
	for infosession in current_infosessions:
		# Check the time
		# new_start = datetime.datetime.strptime(new_start_time, '%H:%M')
		new_start_seconds = new_start_time.hour * 3600 + new_start_time.minute * 60
		# new_end = datetime.datetime.strptime(new_end_time, '%H:%M')
		new_end_seconds = new_end_time.hour * 3600 + new_end_time.minute * 60

		# old_start = datetime.datetime.strptime(booth.time_start, '%H:%M')
		old_start_seconds = infosession.start_time.hour * 3600 + infosession.start_time.minute * 60
		# old_end = datetime.datetime.strptime(booth.time_end, '%H:%M')
		old_end_seconds = infosession.end_time.hour * 3600 + infosession.end_time.minute * 60
		# First case is if our new event starts during the potential conflicted event
		# Second case is if our new event ends during the potential conflicted event
		if((new_start_seconds >= old_start_seconds and 
			new_start_seconds <= old_end_seconds) or
			(new_end_seconds >= old_start_seconds and new_end_seconds <= old_end_seconds)):
			return False
	return True

class AutocompleteUni(autocomplete.Select2ListView):
    def get_list(self):
        return uni_list()

def signup(request, slot_id):
	slot = get_object_or_404(KeyVal, pk=slot_id)
	signup_dictionary = get_list_or_404(KeyVal, container=get_object_or_404(Dictionary_Booth,
																			career_booth=slot.container.career_booth))
	user = request.user

	if slot.value != None:
		messages.error(request, ("Sorry! Someone already signed up for this slot."))
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	for time in signup_dictionary:
		if time.value == user:
			messages.error(request, ("Sorry! You've already signed up for this booth."))
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	if not available(request, slot_id):
		messages.error(request, ("Sorry! It looks like you have a scheduling conflict with another booth. Please note that there must be at least a minute buffer between interviews."))
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	slot.value = user
	slot.save()
	messages.success(request, ('You have successfully signed up for this time slot!'))
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def change(request, slot_id):
	slot = get_object_or_404(KeyVal, pk=slot_id)
	signup_dictionary = get_list_or_404(KeyVal, container=get_object_or_404(Dictionary_Booth,
																			career_booth=slot.container.career_booth))
	user = request.user

	if slot.value != None:
		messages.error(request, ("Sorry! Someone already signed up for this slot."))
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	if not available(request, slot_id):
		messages.error(request, ("Sorry! It looks like you have a scheduling conflict with another booth. Please note that there must be at least a minute buffer between interviews."))
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	for time in signup_dictionary:
		if time.value == user:
			time.value = None
			slot.value = user
			time.save()
			slot.save()
			messages.success(request, ('You have successfully signed up for this time slot!'))
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove(request, slot_id):
	slot = get_object_or_404(KeyVal, pk=slot_id)
	user = request.user

	if slot.value == user:
		slot.value = None
		messages.success(request, ("You've successfully unregistered from this time slot!"))
	else:
		messages.error(request, ("Sorry! You don't appear to be in this time slot!"))
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	slot.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def getDateRangeFromWeek(p_year,p_week):

    firstdayofweek = datetime.datetime.strptime(f'{p_year}-W{int(p_week )- 1}-1', "%Y-W%W-%w").date()
    lastdayofweek = firstdayofweek + datetime.timedelta(days=6.9)
    return firstdayofweek, lastdayofweek

def time_slots(start_time, end_time, interview_duration, rest_duration):
	student_duration = interview_duration + rest_duration
	t = start_time
	while t <= (datetime.datetime.combine(datetime.date.today(), end_time)
					- datetime.timedelta(minutes=interview_duration)).time():
		yield t.strftime('%H:%M')
		t = (datetime.datetime.combine(datetime.date.today(), t) +
			datetime.timedelta(minutes=student_duration)).time()

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
		# Check for scheduling conflicts
		if not recruiter_available(request, booth):
			booth.delete()
			messages.error(request, ('You have a scheduling conflict with another event that you have created previously.'))
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
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
				booth.delete()
				messages.error(request, ('You have a scheduling conflict with another event that you have created previously.'))
				return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

		booth.career_fair = fair
		
		# Set up booth_name
		if booth.booth_name == None:
			booth.booth_name = booth.company + "Booth" 

		""" code below will create dictionary for signup """

		dictionary = Dictionary_Booth.objects.create(
			career_booth = booth
		)

		signup_slots = list(
			time_slots(
				booth.time_start, booth.time_end, booth.interview_duration, booth.rest_duration
			)
		)

		""" Keyval values"""
		for time in signup_slots:
			t = datetime.datetime.strptime(time,'%H:%M') 
			time_end = (t + datetime.timedelta(minutes=booth.interview_duration))
			time_end = time_end.strftime('%H:%M')
			KeyVal.objects.create(container=dictionary, key=time, end=time_end, value=None)

		# for time in signup_slots:
		# 	KeyVal.objects.create(container=dictionary, key=time, value=None)

		"""Here is the Zoom link creation"""
		with ZoomClient('BLKlHrYJQE2Zfc5VN7YgmQ', 'X729m575QKEgWrymCCNjICxE13TJTfzf43sO') as client:
			date_str = str(booth.date)
			time_str = str(booth.time_start)
			year = int(date_str[:4])
			month = int(date_str[5:7])
			day = int(date_str[8:])
			HH = int(time_str[:2])
			MM = int(time_str[3:5])
			SS = 00
			startTime = datetime.datetime(year,month,day,HH,MM,SS)
			create_meeting_response = client.meeting.create(user_id='me', start_time = startTime)
			create_meeting_json = create_meeting_response.json()
			booth.join_zoom_url = create_meeting_json['join_url']
			booth.start_zoom_url = create_meeting_json['start_url']

		form.save()
		messages.success(request, ('You have successfully signed up for a booth at a career fair'))
		return HttpResponseRedirect('/career_fair')

def detail(request, event_id):
	career_fair = get_object_or_404(Career_Fair, pk=event_id)
	booths = Career_Booth.objects.filter(career_fair = career_fair)
	user_booths, other_booths, zoom_time = [], [], {}
	if request.user.is_student:
		for booth in booths:
			dictionary = get_object_or_404(Dictionary_Booth, career_booth=booth)
			student = KeyVal.objects.filter(container=dictionary, value=request.user)
			if len(student) == 1:
				user_booths.append(booth)
				student_time = datetime.datetime.strptime(student[0].key, '%H:%M')
				student_seconds = student_time.hour * 3600 + student_time.minute * 60
				now = timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone())
				now_seconds = now.hour * 3600 + now.minute * 60
				booth_seconds = booth.interview_duration * 60
				if booth.date == datetime.date.today():
					if student_seconds <= now_seconds and (now_seconds - student_seconds) < booth_seconds:
						zoom_time[booth] = True
				else:
					zoom_time[booth] = False
			else:
				other_booths.append(booth)
				zoom_time[booth] = False
	elif request.user.is_recruiter:
		for booth in booths:
			if booth.recruiter == request.user:
				user_booths.append(booth)
				if booth.date == datetime.date.today():
					zoom_time[booth] = True
				else:
					zoom_time[booth] = False
			else:
				other_booths.append(booth)
				zoom_time[booth] = False

	return render(request, 'career_fair/view_booths.html', {'event': career_fair,
															'user_booths': user_booths,
															'other_booths': other_booths,
															'zoom_time': zoom_time})

def booth_detail(request, event_id, booth_company):
	career_fair = get_object_or_404(Career_Fair, pk=event_id)
	career_booth = get_object_or_404(Career_Booth, company=booth_company, career_fair=career_fair)
	dictionary = get_object_or_404(Dictionary_Booth, career_booth=career_booth)
	signup_list = KeyVal.objects.filter(container=dictionary)
	student = KeyVal.objects.filter(container=dictionary, value=request.user)
	altered_signuplist = []

	if len(student) == 1:
		signedup_slot = student[0]
	else:
		signedup_slot = None

	if career_booth.date >= datetime.date.today(): #if day for event is in the future or today
		for slot in signup_list:
			if slot.value == request.user or slot.value == None:
				altered_signuplist.append(slot)

	if request.user.is_recruiter:
		altered_signuplist = signup_list

	return render(request, 'career_fair/view_booth_details.html', {'booth': career_booth,
																		'signup_list': altered_signuplist,
																		'signedup_slot': signedup_slot})



class BoothError(TemplateView):
	template_name = 'career_fair/booth_creation_error.html'

class CareerFairDashboard(TemplateView):
	template_name = 'career_fair/career_fair_dashboard.html'
	def get_context_data(self, **kwargs):
		request = self.request
		context = super(CareerFairDashboard, self).get_context_data(**kwargs)
		if(request.user.is_student):
			student = Student.objects.filter(user = request.user)[0]
			context['career_list'] = Career_Fair.objects.filter(
				university = student.university, lastdate__gte=datetime.datetime.now() - timedelta(days=1)
			).order_by('firstdate')
			context['past_career_list'] = Career_Fair.objects.filter(
				university = student.university, lastdate__lte=datetime.datetime.now() - timedelta(days=1)
			).order_by('firstdate')
		elif(request.user.is_recruiter):
			recruiter = Recruiter.objects.filter(user = request.user)[0]
			context['career_list'] = Career_Fair.objects.filter(
				lastdate__gte=datetime.datetime.now() - timedelta(days=1)
			).order_by('firstdate')
			context['past_career_list'] = Career_Fair.objects.filter(
				lastdate__lte=datetime.datetime.now() - timedelta(days=1)
			).order_by('firstdate')
			print(datetime.datetime.now() - timedelta(days=1))
			# context['joined_fairs'] = Career_Fair.objects.filter()
		return context

class DeleteBoothConfirmation(TemplateView):
	template_name = 'career_fair/delete_booth_confirmation.html'

def DeleteBooth(request, booth_id):
	booth = get_object_or_404(Career_Booth, pk=booth_id)
	career_fair = get_object_or_404(Career_Fair, pk = booth.career_fair.id)
	booth.delete()
	if(len(Career_Booth.objects.filter(career_fair = booth.career_fair)) == 0):
		career_fair.delete()
	messages.success(request, ('Your booth has been successfully deleted.'))
	return HttpResponseRedirect('/career_fair')
