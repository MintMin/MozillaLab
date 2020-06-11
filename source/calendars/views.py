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
from django.views.generic import TemplateView

from event.models import Event
from accounts.models import Recruiter
from event.forms import CreateEventForm
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta


# @method_decorator(login_required, name='dispatch')
class ViewCalendar(TemplateView):
	template_name = 'calendar/view_calendar.html'

	def get_context_data(self, **kwargs):
		request = self.request
		context = super(ViewCalendar, self).get_context_data(**kwargs)

		if(request.user.is_recruiter):
			context['event_list'] = Event.objects.filter(
			main_recruiter = request.user)

		elif(request.user.is_student):
			context['event_list'] = Event.objects.filter(
			rsvp_list__in = [request.user])

		return context



# @method_decorator(login_required, name='dispatch')
# class ViewCalendar(TemplateView):
#     template_name = 'calendar/view_calendar.html'
#     form_class = EventForm

#     def get_context_data(self, **kwargs):
#         context = super(ViewCalendar, self).get_context_data(**kwargs)
#         context['eventlist'] = Event.objects.all()

	
		# if(request.user.is_recruiter):
		# 	context['event_list'] = Event.objects.filter(
		# 		main_recruiter = request.user, date__gte = datetime.now() - timedelta(days=1)).order_by('date')[:3]
		# elif(request.user.is_student):
		# 	context['event_list'] = Event.objects.filter(
		# 		rsvp_list__in = [request.user], date__gte = datetime.now() - timedelta(days=1)).order_by('date')[:3]

	# 	if (request.user.is_recruiter):
	# 		context['past_event_list'] = Event.objects.filter(
	# 			main_recruiter=request.user, date__lte=datetime.now() - timedelta(days=1)).order_by('date')[:3]
	# 	elif (request.user.is_student):
	# 		context['past_event_list'] = Event.objects.filter(
	# 			rsvp_list__in=[request.user], date__lte=datetime.now() - timedelta(days=1)).order_by('date')[:3]

        # return context




