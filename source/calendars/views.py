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
# from django.shortcuts import get_object_or_404, get_list_or_404

from event.models import Event
from accounts.models import Student, Recruiter
from career_fair.models import Career_Fair, Career_Booth, Dictionary_Booth, KeyVal

from event.forms import CreateEventForm
from django.http import HttpResponseRedirect

import time
import datetime
from datetime import datetime, timedelta



class ViewCalendar(TemplateView):
    template_name = 'calendar/view_calendar.html'

    def get_context_data(self, **kwargs):
        request = self.request
        context = super(ViewCalendar, self).get_context_data(**kwargs)

        if(request.user.is_recruiter):
            context['event_list'] = Event.objects.filter(
                main_recruiter = request.user, date__gte = datetime.now()-timedelta(days=1))
            context['past_event_list'] = Event.objects.filter(
                main_recruiter = request.user, date__lte = datetime.now()-timedelta(days=1))

            recruiter = Recruiter.objects.filter(user = request.user)[0]
            context['career_list'] = Career_Fair.objects.filter(
                lastdate__gte=datetime.now() - timedelta(days=1))  # last day greater than today     
            context['past_career_list'] = Career_Fair.objects.filter(
                lastdate__lte=datetime.now() - timedelta(days=1))

            context['booth_list'] = Career_Booth.objects.filter(
                recruiter = request.user, date__gte=datetime.now() - timedelta(days=1))  
            context['past_booth_list'] = Career_Booth.objects.filter(
                recruiter = request.user, date__lte=datetime.now() - timedelta(days=1))
            
            # booths = Career_Booth.objects.filter(
            #     recruiter = request.user, date__gte=datetime.now() - timedelta(days=1))  # only show future interviews
            # user_booths, other_booths = [], []
            # for booth in booths:
            #     dictionary = get_object_or_404(Dictionary_Booth, career_booth=booth)
            #     student = KeyVal.objects.filter(container=dictionary, value = None)

            
            # context['interview_list'] = KeyVal.objects.filter(container=dictionary, key=time, value=None)

        elif(request.user.is_student):
            context['event_list'] = Event.objects.filter(
                rsvp_list__in = [request.user],date__gte = datetime.now()-timedelta(days=1))
            context['past_event_list'] = Event.objects.filter(
                rsvp_list__in = [request.user],date__lte = datetime.now()-timedelta(days=1))
            
            student = Student.objects.filter(user = request.user)[0]
            context['career_list'] = Career_Fair.objects.filter(
                university = student.university, lastdate__gte=datetime.now() - timedelta(days=1)) # last day greater than today
            context['past_career_list'] = Career_Fair.objects.filter(
                university = student.university, lastdate__lte=datetime.now() - timedelta(days=1))

            # context['interview']  = KeyVal.objects.filter(value = request.user)

            # user = request.user
            # signup = KeyVal.objects.filter(value = user)[0]
            # start = signup.key
            # signup_dic = signup[0]
            # career_fair = signup_dic.container.career_booth.career_fair
            # date = signup_dic.container.career_booth.date
            # duration = signup.container.career_booth.interview_duration
            # end = start + duration 

        return context

    # def get_time(self, **kwargs):
    #   request = self.request
    #   context = super(ViewCalendar, self).get_time(**kwargs)



