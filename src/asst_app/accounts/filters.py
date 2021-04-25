import django_filters
from django_filters import DateFilter, TimeFilter, CharFilter, NumberFilter
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