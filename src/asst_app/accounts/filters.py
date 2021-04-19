import django_filters
from django_filters import DateFilter, TimeFilter, CharFilter
from .models import *

class ValidVisitorFilter(django_filters.FilterSet):
    name = CharFilter(field_name="name", lookup_expr='icontains')
    entry_date = DateFilter(field_name="entry_date", lookup_expr='gte')
    entry_time = TimeFilter(field_name="entry_time", lookup_expr='gte')
    class Meta:
        model = ValidVisitor
        fields = '__all__'
        exclude = ['soc_name']