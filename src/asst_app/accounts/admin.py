from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Society)
admin.site.register(ValidVisitor)
admin.site.register(InvalidVisitor)
admin.site.register(NewVisitor)
