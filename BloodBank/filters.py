import django_filters
from .models import *
from django_filters import CharFilter

class EventFilter(django_filters.FilterSet):
    Name= CharFilter(field_name='eventname',
                               lookup_expr='icontains')
    class Meta:
        model= Events
        fields= ''