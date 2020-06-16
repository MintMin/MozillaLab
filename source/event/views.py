from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LogoutView as BaseLogoutView, PasswordChangeView as BasePasswordChangeView,
    PasswordResetDoneView as BasePasswordResetDoneView, PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from django.shortcuts import get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, FormView
from django.conf import settings
from django.views.generic import TemplateView, CreateView
from .models import Event
from accounts.models import Recruiter
from career_fair.models import KeyVal, Career_Booth
from .forms import CreateEventForm
import json
from zoomus import ZoomClient
from django.utils.dateparse import parse_datetime
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
from django.utils import timezone

def student_available(request, event_id):
	new_infosession = Event.objects.filter(pk = event_id)[0]
	user = request.user
	date = new_infosession.date
	# First check conflicts with career fair
	current_slots = KeyVal.objects.filter(value = user)
	for keyval in current_slots:
		if(keyval.container.career_booth.date == date):
			# Check the time
			new_start_seconds = new_infosession.start_time.hour * 3600 + new_infosession.start_time.minute * 60
			# new_end = datetime.datetime.strptime(new_end_time, '%H:%M')
			new_end_seconds = new_infosession.end_time.hour * 3600 + new_infosession.end_time.minute * 60

			time_pot_conflict = datetime.strptime(keyval.key, '%H:%M')
			start_seconds_pot_conflict = time_pot_conflict.hour * 3600 + time_pot_conflict.minute * 60
			duration_pot_conflict = (1 + keyval.container.career_booth.interview_duration) * 60
			total_conflict = start_seconds_pot_conflict + duration_pot_conflict
			# First case is if our new event starts during the potential conflicted event
			# Second case is if our new event ends during the potential conflicted event
			if((new_start_seconds >= start_seconds_pot_conflict and 
				new_start_seconds <= total_conflict) or
				(new_end_seconds >= start_seconds_pot_conflict and new_end_seconds <= total_conflict)):
				return False
	# Next, check conflicts with infosessions
	current_infosessions = Event.objects.filter(rsvp_list__in = [user], date = date)
	for infosession in current_infosessions:
		# Check the time
		new_start_seconds = new_infosession.start_time.hour * 3600 + new_infosession.start_time.minute * 60
		# new_end = datetime.datetime.strptime(new_end_time, '%H:%M')
		new_end_seconds = new_infosession.end_time.hour * 3600 + new_infosession.end_time.minute * 60


		old_start_seconds = infosession.start_time.hour * 3600 + infosession.start_time.minute * 60
		old_end_seconds = infosession.end_time.hour * 3600 + infosession.end_time.minute * 60
		# First case is if our new event starts during the potential conflicted event
		# Second case is if our new event ends during the potential conflicted event
		if((new_start_seconds >= old_start_seconds and 
			new_start_seconds <= old_end_seconds) or
			(new_end_seconds >= old_start_seconds and new_end_seconds <= old_end_seconds)):
			return False
	return True

def recruiter_available(request, infosession):
	new_infosession = infosession
	recruiter = request.user
	date = new_infosession.date
	new_start_time = new_infosession.start_time
	new_end_time = new_infosession.end_time
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

def detail(request, event_id):
	event = get_object_or_404(Event, pk=event_id)
	rsvp = True
	if(event in Event.objects.filter(rsvp_list__in = [request.user])):
		rsvp = False
	past = False
	if(event.date < datetime.now().date()):
		past = True
	return render(request, 'event/view_event.html', {'event': event, 'rsvp_bool': rsvp, 'past':past})

def rsvp(request, event_id):
	event = get_object_or_404(Event, pk=event_id)
	user = request.user
	if event.space_open != 0:
		if not student_available(request, event_id):
			messages.error(request, ("Sorry! It looks like you have a scheduling conflict with another event. Please note that there must be at least a minute buffer around events."))
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		event.rsvp_list.add(user)
		event.space_open -= 1
		event.save()
		messages.success(request, _('You have successfully rsvpd for the event'))
	else:
		messages.error(request, _('Sorry! All spaces have been filled,'))
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def un_rsvp(request, event_id):
	event = get_object_or_404(Event, pk=event_id)
	user = request.user
	event.rsvp_list.remove(user)
	event.space_open += 1
	event.save()
	messages.success(request, _('You have successfully unregistered to the event'))
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_event(request, event_id):
	event = get_object_or_404(Event, pk=event_id)
	event.delete()
	messages.success(request, _('You have successfully deleted your event!'))
	return HttpResponseRedirect('/event')

class ViewEvent(TemplateView):
    template_name = 'event/view_event.html'

class EventDashboard(TemplateView):
	template_name = 'event/event_dashboard.html'
	def get_context_data(self, **kwargs):
		request = self.request
		context = super(EventDashboard, self).get_context_data(**kwargs)
		not_in_event_list, counter, zoom_time = [], 0, {}
		now = timezone.make_aware(datetime.now(),timezone.get_default_timezone())
		if(request.user.is_recruiter):
			context['event_list'] = Event.objects.filter(
				main_recruiter = request.user, date__gte = datetime.now() - timedelta(days=1)).order_by('date')[:3]
		elif(request.user.is_student):
			context['event_list'] = Event.objects.filter(
				rsvp_list__in = [request.user], date__gte = datetime.now() - timedelta(days=1)).order_by('date')[:3]
		for i in context['event_list']:
			now_seconds = now.hour * 3600 + now.minute * 60
			info_start_seconds = i.start_time.hour * 3600 + i.start_time.minute * 60
			info_end_seconds = i.end_time.hour * 3600 + i.end_time.minute * 60
			if str(i.date) == now.strftime('%Y-%m-%d'):
				if info_start_seconds <= (now_seconds + 300) and now_seconds < info_end_seconds:
					zoom_time[i] = True
				else:
					zoom_time[i] = False
			else:
				zoom_time[i] = False
		context['zoom_time'] = zoom_time

		for i in Event.objects.filter(date__gte = datetime.now() - timedelta(days=1)).order_by('date'):
			if counter == 6:
				break
			if i not in context['event_list']:
				counter += 1
				not_in_event_list.append(i)

		context['all_events'] = not_in_event_list

		if (request.user.is_recruiter):
			context['past_event_list'] = Event.objects.filter(
				main_recruiter=request.user, date__lte=datetime.now() - timedelta(days=1)).order_by('date')[:3]
		elif (request.user.is_student):
			context['past_event_list'] = Event.objects.filter(
				rsvp_list__in=[request.user], date__lte=datetime.now() - timedelta(days=1)).order_by('date')[:3]

		return context

# do I need to name a new class for event list page???
class EventList(TemplateView):
	template_name = 'event/event_list.html'
	def get_context_data(self, **kwargs):
		request = self.request
		context = super(EventList, self).get_context_data(**kwargs)
		context['all_events'] = Event.objects.filter(
			date__gte = datetime.now() - timedelta(days=1)
		).order_by('date')
		return context

class MyEventList(TemplateView):
	template_name = 'event/my_event_list.html'
	def get_context_data(self, **kwargs):
		request = self.request
		context = super(MyEventList, self).get_context_data(**kwargs)
		zoom_time = {}
		now = timezone.make_aware(datetime.now(),timezone.get_default_timezone())
		if(request.user.is_recruiter):
			context['event_list'] = Event.objects.filter(
				main_recruiter = request.user, date__gte = datetime.now() - timedelta(days=1)).order_by('date')
		elif(request.user.is_student):
			context['event_list'] = Event.objects.filter(
				rsvp_list__in = [request.user], date__gte = datetime.now() - timedelta(days=1)).order_by('date')
		for i in context['event_list']:
			now_seconds = now.hour * 3600 + now.minute * 60
			info_start_seconds = i.start_time.hour * 3600 + i.start_time.minute * 60
			info_end_seconds = i.end_time.hour * 3600 + i.end_time.minute * 60
			if str(i.date) == now.strftime('%Y-%m-%d'):
				if info_start_seconds <= (now_seconds + 300) and now_seconds < info_end_seconds:
					zoom_time[i] = True
				else:
					zoom_time[i] = False
			else:
				zoom_time[i] = False
		context['zoom_time'] = zoom_time
		return context

class CreateEvent(CreateView):
	template_name = 'event/create_event.html'
	model = Event
	form_class = CreateEventForm
	def save(self, *args, **kwargs):
		self.absolute_url = self.get_absolute_url()
		super(event, self).save(*args, **kwargs)

	def form_valid(self, form):
		event = form.save()
		request = self.request
		event.main_recruiter = request.user
		# Check for scheduling conflicts
		if not recruiter_available(request, event):
			messages.error(request, ('You have a scheduling conflict with another event that you have created previously.'))
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		event.space_open = event.rsvp_capacity
		with ZoomClient('BLKlHrYJQE2Zfc5VN7YgmQ', 'X729m575QKEgWrymCCNjICxE13TJTfzf43sO') as client:
			date_str = str(event.date)
			time_str = str(event.start_time)
			year = int(date_str[:4])
			month = int(date_str[5:7])
			day = int(date_str[8:])
			HH = int(time_str[:2])
			MM = int(time_str[3:5])
			SS = 00
			startTime = datetime(year,month,day,HH,MM,SS)
			create_meeting_response = client.meeting.create(user_id='me', start_time = startTime)
			create_meeting_json = create_meeting_response.json()
			event.join_zoom_url = create_meeting_json['join_url']
			event.start_zoom_url = create_meeting_json['start_url']
		#print(create_meeting_json)
		form.save()
		messages.success(request, _('You have successfully created your event'))
		return HttpResponseRedirect('/event')

class PastEventList(TemplateView):
	template_name = 'event/past_event.html'
	def get_context_data(self, **kwargs):
		request = self.request
		context = super(PastEventList, self).get_context_data(**kwargs)
		if(request.user.is_recruiter):
			context['past_event_list'] = Event.objects.filter(
				main_recruiter = request.user, date__lte = datetime.now() - timedelta(days=1)).order_by('date')
		elif(request.user.is_student):
			context['past_event_list'] = Event.objects.filter(
				rsvp_list__in = [request.user], date__lte = datetime.now() - timedelta(days=1)).order_by('date')
		return context