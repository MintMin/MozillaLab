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



# class RunSearch(TemplateView):
#     template_name = 'search/run_search.html'

    # def search(self,request):
    #     keyword = request.GET.get('keyword')                    # get and save the keyword via request.GET (like python dictionary)
    #     error_msg = ''

    #     if not keyword:
    #         error_msg = 'Please enter a keyword'
    #         return render(request, 'search/run_search.html', {'error_msg': error_msg})

    #     result_list = Event.objects.filter(title__icontains=keyword)   # i: ... icontains -- field lookups
    #     return render(request, 'search/run_search.html', {'error_msg': error_msg,'result_list': result_list})

def run_search(request):
        keyword = request.GET.get('keyword')                    # get and save the keyword via request.GET (like python dictionary)
        error_msg = ''

        if not keyword:
            error_msg = 'Please enter a keyword'
            return render(request, 'search/run_search.html', {'error_msg': error_msg})

        result_list = Event.objects.filter(title__icontains=keyword)   # i: ... icontains -- field lookups
        return render(request, 'search/run_search.html', {'error_msg': error_msg,'result_list': result_list})


# def filter(request,*args,**kwargs):

#     print(kwargs)

#     condition = {}

#     for k,v in kwargs.items():
#         kwargs[k] = int(v)
#         if v == "0":
#             pass
#         else:
#             condition[k] = v

#     type_list = Event.objects.values('Event_type')
#     # recruiter_list = Event.objects.all(main_recruiter__icontains=keyword)
#     # company_list = Event.objects.all(company__icontains=keyword)
#     # job_list = Category.objects.all()
#     # date filter

# # result = models.Article.objects.filter(article_type_id=kwargs["article_type_id"],category_id=kwargs["category_id"])

#     result = Event.objects.filter(**condition)
    
#     return render(request,'article.html',{
#                         'result':result,
#                         'type_list':type_list,
#                         # 'category_list':category_list,
#                         'arg_dict':kwargs,
#                     })
