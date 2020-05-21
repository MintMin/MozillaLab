from django.contrib import admin

# Register your models here.
from event.models import Recruiter, Company, Event

# ,Type

admin.site.register(Event)
admin.site.register(Recruiter)
admin.site.register(Company)
# admin.site.register(Type)