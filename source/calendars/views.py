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
    
        return context

    # def get_time(self, **kwargs):
    #   request = self.request
    #   context = super(ViewCalendar, self).get_time(**kwargs)





# DISPLAY CAREER FAIR/BOOTHS
# def get_context_data(self, **kwargs):
#       request = self.request
#       context = super(CareerFairDashboard, self).get_context_data(**kwargs)
#       if(request.user.is_student):
#           student = Student.objects.filter(user = request.user)[0]
#           context['career_list'] = Career_Fair.objects.filter(
#               university = student.university, firstdate__gte=datetime.datetime.now() - timedelta(days=1)
#           ).order_by('firstdate')
#           context['past_career_list'] = Career_Fair.objects.filter(
#               university = student.university, lastdate__lte=datetime.datetime.now() - timedelta(days=1)
#           ).order_by('firstdate')
#       elif(request.user.is_recruiter):
#           recruiter = Recruiter.objects.filter(user = request.user)[0]
#           context['career_list'] = Career_Fair.objects.filter(
#               firstdate__gte=datetime.datetime.now() - timedelta(days=1)
#           ).order_by('firstdate')
#           context['past_career_list'] = Career_Fair.objects.filter(
#               lastdate__lte=datetime.datetime.now() - timedelta(days=1)
#           ).order_by('firstdate')
#           # context['joined_fairs'] = Career_Fair.objects.filter()
#       return context

#   def detail(request, event_id):
#       career_fair = get_object_or_404(Career_Fair, pk=event_id)
#       booths = Career_Booth.objects.filter(career_fair = career_fair)
#       user_booths, other_booths, zoom_time = [], [], {}
#       if request.user.is_student:
#           for booth in booths:
#               dictionary = get_object_or_404(Dictionary_Booth, career_booth=booth)
#               student = KeyVal.objects.filter(container=dictionary, value=request.user)
#               if len(student) == 1:
#                   user_booths.append(booth)
#                   # student_time = datetime.datetime.strptime(student[0].key, '%H:%M')
#                   # student_seconds = student_time.hour * 3600 + student_time.minute * 60
#                   # now = datetime.datetime.now().time()
#                   # now_seconds = now.hour * 3600 + now.minute * 60
#                   # booth_seconds = booth.interview_duration * 60
                    
#                   # if booth.date == datetime.date.today():
#                       # if student_seconds <= now_seconds and (now_seconds - student_seconds) < booth_seconds:
#                           # zoom_time[booth] = True
                    
#               else:
#                   other_booths.append(booth)          
                    
#       elif request.user.is_recruiter:
#           for booth in booths:
#               if booth.recruiter == request.user:
#                   user_booths.append(booth)
#                   # if booth.date == datetime.date.today():
#                   #   zoom_time[booth] = True
#                   # else:
#                   #   zoom_time[booth] = False
#               else:
#                   other_booths.append(booth)
#                   # zoom_time[booth] = False

# class CareerFairDashboard(TemplateView):
#   template_name = 'career_fair/career_fair_dashboard.html'
#   def get_context_data(self, **kwargs):
#       request = self.request
#       context = super(CareerFairDashboard, self).get_context_data(**kwargs)
#       if(request.user.is_student):
#           student = Student.objects.filter(user = request.user)[0]
#           context['career_list'] = Career_Fair.objects.filter(
#               university = student.university, firstdate__gte=datetime.datetime.now() - timedelta(days=1)
#           ).order_by('firstdate')
#           context['past_career_list'] = Career_Fair.objects.filter(
#               university = student.university, lastdate__lte=datetime.datetime.now() - timedelta(days=1)
#           ).order_by('firstdate')
#       elif(request.user.is_recruiter):
#           recruiter = Recruiter.objects.filter(user = request.user)[0]
#           context['career_list'] = Career_Fair.objects.filter(
#               firstdate__gte=datetime.datetime.now() - timedelta(days=1)
#           ).order_by('firstdate')
#           context['past_career_list'] = Career_Fair.objects.filter(
#               lastdate__lte=datetime.datetime.now() - timedelta(days=1)
#           ).order_by('firstdate')
#           # context['joined_fairs'] = Career_Fair.objects.filter()
#       return context




