from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group

class SocDisplay(admin.ModelAdmin):
    list_display  = ['name', 'sec_name', 'address']

class ValVisitDisplay(admin.ModelAdmin):
    list_display  = ['name', 'entry_date', 'temp', 'soc_name']

class InvalVisitDisplay(admin.ModelAdmin):
    list_display  = ['name', 'entry_date', 'status', 'soc_name']

class NewVisitDisplay(admin.ModelAdmin):
    list_display  = ['name', 'soc_name']

admin.site.unregister(Group)

admin.site.register(Society, SocDisplay)
admin.site.register(ValidVisitor, ValVisitDisplay)
admin.site.register(InvalidVisitor, InvalVisitDisplay)
admin.site.register(NewVisitor, NewVisitDisplay)

admin.site.site_header = "SecuroTech Administration"