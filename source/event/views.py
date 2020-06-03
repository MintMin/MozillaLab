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
from .forms import CreateEventForm
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta

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
		not_in_event_list, counter = [], 0
		if(request.user.is_recruiter):
			context['event_list'] = Event.objects.filter(
				main_recruiter = request.user, date__gte = datetime.now() - timedelta(days=1)).order_by('date')[:3]
		elif(request.user.is_student):
			context['event_list'] = Event.objects.filter(
				rsvp_list__in = [request.user], date__gte = datetime.now() - timedelta(days=1)).order_by('date')[:3]

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
		if(request.user.is_recruiter):
			context['event_list'] = Event.objects.filter(
				main_recruiter = request.user, date__gte = datetime.now() - timedelta(days=1)).order_by('date')
		elif(request.user.is_student):
			context['event_list'] = Event.objects.filter(
				rsvp_list__in = [request.user], date__gte = datetime.now() - timedelta(days=1)).order_by('date')
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
		event.space_open = event.rsvp_capacity
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