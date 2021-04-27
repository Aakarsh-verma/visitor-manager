import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter, ChoiceFilter
from .models import *
from django import forms

class ValidVisitorFilter(django_filters.FilterSet):
    name = CharFilter(field_name="name", lookup_expr='icontains')
    entry_date = DateFilter(field_name="entry_date", lookup_expr='gte')
    temp = NumberFilter(field_name="temp", lookup_expr='gte')
       
    class Meta:
        model = ValidVisitor
        fields = '__all__'
        exclude = ['entry_time','soc_name']

class InvalidVisitorFilter(django_filters.FilterSet):
    STATUS_CHOICES = (
        ('No Mask', 'No Mask'),
        ('High Temperature', 'High Temperature'),
    )

    name = CharFilter(field_name="name", lookup_expr='icontains')
    entry_date = DateFilter(field_name="entry_date", lookup_expr='gte')
    status =  ChoiceFilter(choices=STATUS_CHOICES)
       
    class Meta:
        model = InvalidVisitor
        fields = '__all__'
        exclude = ['entry_time','temp', 'soc_name']