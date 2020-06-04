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
import json
from zoomus import ZoomClient
from datetime import datetime

def detail(request, event_id):
	event = get_object_or_404(Event, pk=event_id)
	rsvp = True
	if(event in Event.objects.filter(rsvp_list__in = [request.user])):
		rsvp = False
	return render(request, 'event/view_event.html', {'event': event, 'rsvp_bool':rsvp})

def rsvp(request, event_id):
	event = get_object_or_404(Event, pk=event_id)
	user = request.user
	event.rsvp_list.add(user)
	# if(event.rsvp_list.filter(rsvp_list__in = [user])):
	messages.success(request, _('You have successfully rsvpd for the event'))
	return redirect('index')

class ViewEvent(TemplateView):
    template_name = 'event/view_event.html'

class ExampleEvent(TemplateView):
    template_name = 'event/example_event.html'

class EventDashboard(TemplateView):
	template_name = 'event/event_dashboard.html'
	def get_context_data(self, **kwargs):
		request = self.request
		context = super(EventDashboard, self).get_context_data(**kwargs)
		if(request.user.is_recruiter):
			context['event_list'] = Event.objects.filter(main_recruiter = request.user)
		elif(request.user.is_student):
			context['event_list'] = Event.objects.filter(rsvp_list__in = [request.user])
		context['all_events'] = Event.objects.all()
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
		with ZoomClient('BLKlHrYJQE2Zfc5VN7YgmQ', 'X729m575QKEgWrymCCNjICxE13TJTfzf43sO') as client:
			startTime = datetime(2020,5,28,3,00,00)
			create_meeting_response = client.meeting.create(user_id='me')
			create_meeting_json = create_meeting_response.json()
			print(create_meeting_json)
			event.zoom_url = create_meeting_json['join_url']

    	
		form.save()
		messages.success(request, _('You have successfully created your event'))
		return redirect('index')
