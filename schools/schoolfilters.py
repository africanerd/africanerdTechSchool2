import django_filters
from .models import *


class SchoolFilter(django_filters.FilterSet):
    CHOICES = (('ascending', 'Date added (oldest)'),
               ('descending', 'Date added (newest)'))

    sorting = django_filters.ChoiceFilter(label='Sorting', empty_label='Sort By', choices=CHOICES, method='filter_by_order')

    school_name = django_filters.CharFilter(label='Name', lookup_expr='icontains')
    category = django_filters.ModelChoiceFilter(label='Category', empty_label='Select All Categories', field_name='schooltype',
                                                queryset=SchoolType.objects.filter(school__school_status='AC').distinct())
    city = django_filters.ModelChoiceFilter(label='City', empty_label='Select All Cities', field_name='address__city',
                                            queryset=City.objects.filter(schooladdress__school__school_status='AC').distinct())
    country = django_filters.ModelChoiceFilter(label='Country', empty_label='Select All Countries', field_name='address__city__country',
                                               queryset=Country.objects.filter(
                                                   city__schooladdress__school__school_status='AC').distinct())
    region = django_filters.ModelChoiceFilter(label='Region', empty_label='Select All Regions',
                                              field_name='address__city__country__region',
                                              queryset=Region.objects.filter(
                                                   country__city__schooladdress__school__school_status='AC').distinct())

    class Meta:
        model = School
        fields = ['school_name', 'category', 'city', 'country',
                  'region']

    def filter_by_order(self, queryset, name, value):
        expression = 'school_pub_date' if value == 'ascending' else '-school_pub_date'
        return queryset.order_by(expression)
