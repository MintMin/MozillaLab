from django.contrib import admin

# Register your models here.
from search.models import Recruiter, Company, Type, Event

admin.site.register(Event)
admin.site.register(Recruiter)
admin.site.register(Company)
admin.site.register(Type)
