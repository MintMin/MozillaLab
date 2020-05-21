from django.urls import path

from .views import (
    LogInView, ResendActivationCodeView, RemindUsernameView, RecruiterSignUpView, SignUpView, ActivateView, LogOutView,
    ChangeEmailView, ChangeEmailActivateView, ChangeProfileView, ChangePasswordView,
    RestorePasswordView, RestorePasswordDoneView, RestorePasswordConfirmView, StudentSignUpView
)

from django.conf.urls import url
from .views import (
    StudentProfileView, AutocompleteMajor, AutocompleteUni, AutocompleteCareerInt
)
app_name = 'accounts'

urlpatterns = [
    path('log-in/', LogInView.as_view(), name='log_in'),
    path('log-out/', LogOutView.as_view(), name='log_out'),

    path('resend/activation-code/', ResendActivationCodeView.as_view(), name='resend_activation_code'),

    path('recruiter-sign-up/', RecruiterSignUpView.as_view(), name='recruiter_sign_up'),
    path('student-sign-up/', StudentSignUpView.as_view(), name='student_sign_up'),
    path('activate/<code>/', ActivateView.as_view(), name='activate'),

    path('restore/password/', RestorePasswordView.as_view(), name='restore_password'),
    path('restore/password/done/', RestorePasswordDoneView.as_view(), name='restore_password_done'),
    path('restore/<uidb64>/<token>/', RestorePasswordConfirmView.as_view(), name='restore_password_confirm'),

    path('remind/username/', RemindUsernameView.as_view(), name='remind_username'),
    

    path('change/profile/', ChangeProfileView.as_view(), name='change_profile'),
    path('change/password/', ChangePasswordView.as_view(), name='change_password'),
    path('change/email/', ChangeEmailView.as_view(), name='change_email'),
    path('change/email/<code>/', ChangeEmailActivateView.as_view(), name='change_email_activation'),

    path('student-profile', StudentProfileView.as_view(), name='student-profile'),
    url(r'^major-autocomplete/$', AutocompleteMajor.as_view(), name='major-autocomplete'),
    url(r'^uni-autocomplete/$', AutocompleteUni.as_view(), name='uni-autocomplete'),
    url(r'^career-autocomplete/$', AutocompleteCareerInt.as_view(), name='career-autocomplete'),

    # path('', AccountSettings.as_view(), name='account_settings'),
]
