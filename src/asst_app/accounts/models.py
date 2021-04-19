from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import date
from datetime import time,timedelta
# Create your models here.

class Society(models.Model):
    name = models.CharField(max_length=200)
    sec_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ValidVisitor(models.Model):
    name = models.CharField(max_length=200)
    entry_date = models.DateField(auto_now=False, auto_now_add=False)
    entry_time = models.TimeField(auto_now=False, auto_now_add=False)
    temp = models.FloatField()
    soc_name = models.ForeignKey(Society, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class InvalidVisitor(models.Model):
    STATUS = (
        ('No Mask', 'No Mask'),
        ('High Temperature', 'High Temperature'),
    )
    name = models.CharField(max_length=200)
    entry_date = models.DateField(auto_now=False, auto_now_add=False)
    entry_time = models.TimeField(auto_now=False, auto_now_add=False)
    temp = models.FloatField(null=True, blank=True)
    status =  models.CharField(max_length=50, choices=STATUS)
    soc_name = models.ForeignKey(Society, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class NewVisitor(models.Model):
    name = models.CharField(max_length=200)
    soc_name = models.ForeignKey(Society, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name