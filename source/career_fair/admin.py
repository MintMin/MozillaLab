from django.contrib import admin

# Register your models here.
from .models import Career_Booth, Career_Fair, Dictionary_Booth, KeyVal
# Register your models here.
admin.site.register(Career_Booth)
admin.site.register(Career_Fair)
admin.site.register(Dictionary_Booth)
admin.site.register(KeyVal)