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



class RunSearch(TemplateView):
    template_name = 'search/run_search.html'

    # def get_context_data(self, **kwargs):
    #         context = super(RunSearch, self).get_context_data(**kwargs)
    #         context['event_list'] = Event.objects.all()
    #         return context

# class EventView(TemplateView):
#     # template_name = 'search/student_event.html'
#     template_name = 'main/index.html'
#     def get_context_data(self, **kwargs):
#         context = super(EventView, self).get_context_data(**kwargs)
#         context['event_list'] = Event.objects.all()
#         return context


# class EventView(TemplateView):
#     """
#     A base view for displaying a list of objects.
#     """
#     def get(self, request, *args, **kwargs):
#         self.object_list = self.get_queryset()
#         allow_empty = self.get_allow_empty()

#         if not allow_empty:
#             # When pagination is enabled and object_list is a queryset,
#             # it's better to do a cheap query than to load the unpaginated
#             # queryset in memory.
#             if (self.get_paginate_by(self.object_list) is not None
#                     and hasattr(self.object_list, 'exists')):
#                 is_empty = not self.object_list.exists()
#             else:
#                 is_empty = len(self.object_list) == 0
#             if is_empty:
#                 raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.")
#                         % {'class_name': self.__class__.__name__})
#         context = self.get_context_data()
#         return self.render_to_response(context)

# from search.models import Event

# def index(request):
#     """View function for home page of site."""

#     # Generate counts of some of the main objects
#     event_list = Event.objects.all()

#     context = {
#         'event_list': event_list,
#     }
#     # Render the HTML template index.html with the data in the context variable
#     return render(request, 'index.html', context=context)


# from django.views.generic import ListView

# class EventLobbyView(ListView):
#     model = Event
#     context_object_name = 'my_event_list'   # your own name for the list as a template variable
#     # queryset = Event.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
#     queryset = Event.objects.all
#     template_name = 'search/my_event_list.html'  # Specify your own template name/location