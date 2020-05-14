from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from main.views import IndexPageView, ChangeLanguageView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', IndexPageView.as_view(), name='index'),  # home page!!!

    path('i18n/', include('django.conf.urls.i18n')),
    path('language/', ChangeLanguageView.as_view(), name='change_language'),

    path('accounts/', include('accounts.urls')),

    # student user
    path('student_event/', include('student_event.urls'),name='student_event'),


    
    path('student_infosession/', include('student_infosession.urls'),name='student_infosession'),
    path('student_interview/', include('student_interview.urls'), name='student_interview'),
    path('search/', include('search.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
