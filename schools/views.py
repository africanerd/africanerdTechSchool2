from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.shortcuts import render
from django.db.models import Q
from .models import Region, Continent, SchoolType, SchoolImage, School, SchoolAddress, City, Country
from .schoolfilters import SchoolFilter
from .generalschoolfilter import GeneralSchoolFilter
from rest_framework import viewsets
from .serializers import SchoolSerializer
from django.db.models import Count
from django.core.paginator import Paginator


def home2(request):
    return render(request, 'schools/home2.html')


class IndexView(generic.ListView):
    template_name = 'schools/index.html'
    context_object_name = 'latest_school_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Continent.objects.filter(
            continent_pub_date__lte=timezone.now()
        ).order_by('-continent_pub_date')[:5]


class DetailView(generic.DetailView):
    model = Continent
    template_name = 'schools/detail.html'


class SchoolIndexView(generic.ListView):
    model = SchoolType
    template_name = 'schools/schoolindex.html'
    context_object_name = 'allschooltypes'

    def get_queryset(self):
        return SchoolType.objects.filter(school__school_status='AC').annotate(cats_num=Count('school'))


class SchoolDetailView(generic.DetailView):
    model = SchoolType
    template_name = 'schools/schooldetail.html'

    def get_queryset(self):
        return SchoolType.objects.all()


class SchoolIndexView2(generic.ListView):
    model = School
    queryset = School.objects.prefetch_related(
        'address__city__country__region__continent').filter(school_status='AC')

    # template_name = 'schools/schoolindex2.html'
    template_name = 'schools/schoolbase.html'
    paginate_by = 12

    # set up pagination
    # p = Paginator(School.objects.all(), 2)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['schools'] = School.objects.filter()

        context['schoolfilter'] = SchoolFilter(self.request.GET, queryset=self.get_queryset())
        context['schooltypes'] = SchoolType.objects.filter(school__school_status='AC').annotate(
            cats_num=Count('school')).order_by('-cats_num')[:4]
        context['schoolregions'] = Region.objects.filter(
            country__city__schooladdress__school__school_status='AC').distinct().annotate(
            region_num=Count('country')).order_by('-region_num')
        context['cities'] = City.objects.filter(
            schooladdress__school__school_status='AC').distinct().annotate(
            city_num=Count('schooladdress__school')).order_by('-city_num')[:12]
        context['countries'] = Country.objects.filter(
            city__schooladdress__school__school_status='AC').distinct().annotate(
            country_num=Count('city__schooladdress__school')).order_by('-country_num')[:12]

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return SchoolFilter(self.request.GET, queryset=queryset).qs


class SchoolDetailView2(generic.DetailView):
    model = School
    template_name = 'schools/school-detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation(from parent  class) first to get a context

        context = super().get_context_data(**kwargs)
        # Add a QuerySet in the 'context' of the cars owned by this person

        # context['schoolimages'] = SchoolImage.objects.all
        context['schoolimages'] = SchoolImage.objects.filter(school=self.object)
        context['schooltypes'] = SchoolType.objects.filter(school=self.object)
        # context['schooladdresses'] = SchoolAddress.objects.filter(school=self.object)
        context['schooladdresses'] = SchoolAddress.objects.select_related(
            'city__country__region__continent').filter(
            school=self.object)
        context['schooltypesnav'] = SchoolType.objects.filter(school__school_status='AC').annotate(
            cats_num=Count('school')).order_by('-cats_num')[:4]
        context['schoolregionsnav'] = Region.objects.filter(
            country__city__schooladdress__school__school_status='AC').distinct().annotate(
            region_num=Count('country')).order_by('-region_num')
        context['citiesnav'] = City.objects.filter(
            schooladdress__school__school_status='AC').distinct().annotate(
            city_num=Count('schooladdress__school')).order_by('-city_num')[:12]
        context['countriesnav'] = Country.objects.filter(
            city__schooladdress__school__school_status='AC').distinct().annotate(
            country_num=Count('city__schooladdress__school')).order_by('-country_num')[:12]

        return context


def categoryview(request, cats):
    criterion1 = Q(school__school_status='AC')
    criterion2 = Q(schooltype_name__icontains=cats.replace('-', ' '))
    criterion3 = Q(school_status='AC')
    criterion4 = Q(schooltype__schooltype_name__icontains=cats.replace('-', ' '))
    schooltype = SchoolType.objects.filter(criterion1 & criterion2).distinct()
    school = School.objects.filter(criterion3 & criterion4).distinct()
    schoolfilter = SchoolFilter(request.GET, queryset=School.objects.prefetch_related(
        'address__city__country__region__continent').filter(school_status='AC').distinct())




    schooltypesnav= SchoolType.objects.filter(school__school_status='AC').annotate(
        cats_num=Count('school')).order_by('-cats_num')[:4]
    schoolregionsnav = Region.objects.filter(
        country__city__schooladdress__school__school_status='AC').distinct().annotate(
        region_num=Count('country')).order_by('-region_num')
    citiesnav = City.objects.filter(
        schooladdress__school__school_status='AC').distinct().annotate(
        city_num=Count('schooladdress__school')).order_by('-city_num')[:12]
    countriesnav = Country.objects.filter(
        city__schooladdress__school__school_status='AC').distinct().annotate(
        country_num=Count('city__schooladdress__school')).order_by('-country_num')[:12]
    return render(request, 'schools/school-category.html',
                  {'cats': cats.title().replace('-', ' '), 'schooltypes': schooltype, 'schools': school,
                   'schoolfilter': schoolfilter,
                   'schooltypesnav': schooltypesnav,
                   'schoolregionsnav': schoolregionsnav,
                   'citiesnav': citiesnav,
                   'countriesnav': countriesnav})


def regionview(request, regs):
    criterion1 = Q(country__city__schooladdress__school__school_status='AC')
    criterion2 = Q(region_name__icontains=regs.replace('-', ' '))
    criterion3 = Q(school_status='AC')
    criterion4 = Q(address__city__country__region__region_name__icontains=regs.replace('-', ' '))

    region = Region.objects.filter(criterion1 & criterion2).distinct()
    school = School.objects.filter(criterion3 & criterion4).distinct()

    schoolfilter = SchoolFilter(request.GET, queryset=SchoolType.objects.filter(
        school__school_status='AC').distinct())
    schooltypesnav = SchoolType.objects.filter(school__school_status='AC').annotate(
        cats_num=Count('school')).order_by('-cats_num')[:4]
    schoolregionsnav = Region.objects.filter(
        country__city__schooladdress__school__school_status='AC').distinct().annotate(
        region_num=Count('country')).order_by('-region_num')
    citiesnav = City.objects.filter(
        schooladdress__school__school_status='AC').distinct().annotate(
        city_num=Count('schooladdress__school')).order_by('-city_num')[:12]
    countriesnav = Country.objects.filter(
        city__schooladdress__school__school_status='AC').distinct().annotate(
        country_num=Count('city__schooladdress__school')).order_by('-country_num')[:12]
    return render(request, 'schools/school-region.html',
                  {'regs': regs.title().replace('-', ' '), 'regions': region, 'schools': school,
                   'schoolfilter': schoolfilter,
                   'schooltypesnav': schooltypesnav,
                   'schoolregionsnav': schoolregionsnav,
                   'citiesnav': citiesnav,
                   'countriesnav': countriesnav})


def countryview(request, cnts):
    criterion1 = Q(city__schooladdress__school__school_status='AC')
    criterion2 = Q(country_name__icontains=cnts.replace('-', ' '))
    criterion3 = Q(school_status='AC')
    criterion4 = Q(address__city__country__country_name__icontains=cnts.replace('-', ' '))
    country = Country.objects.filter(criterion1 & criterion2).distinct()
    school = School.objects.filter(criterion3 & criterion4).distinct()

    schoolfilter = SchoolFilter(request.GET, queryset=SchoolType.objects.filter(
        school__school_status='AC').distinct())
    schooltypesnav = SchoolType.objects.filter(school__school_status='AC').annotate(
        cats_num=Count('school')).order_by('-cats_num')[:4]
    schoolregionsnav = Region.objects.filter(
        country__city__schooladdress__school__school_status='AC').distinct().annotate(
        region_num=Count('country')).order_by('-region_num')
    citiesnav = City.objects.filter(
        schooladdress__school__school_status='AC').distinct().annotate(
        city_num=Count('schooladdress__school')).order_by('-city_num')[:12]
    countriesnav = Country.objects.filter(
        city__schooladdress__school__school_status='AC').distinct().annotate(
        country_num=Count('city__schooladdress__school')).order_by('-country_num')[:12]
    return render(request, 'schools/school-country.html',
                  {'countries': cnts.title().replace('-', ' '), 'countries': country, 'schools': school,
                   'schoolfilter': schoolfilter,
                   'schooltypesnav': schooltypesnav,
                   'schoolregionsnav': schoolregionsnav,
                   'citiesnav': citiesnav,
                   'countriesnav': countriesnav})


def cityview(request, cities):
    criterion1 = Q(schooladdress__school__school_status='AC')
    criterion2 = Q(city_name__icontains=cities.replace('-', ' '))
    criterion3 = Q(school_status='AC')
    criterion4 = Q(address__city__city_name__icontains=cities.replace('-', ' '))
    city = City.objects.filter(criterion1 & criterion2).distinct()
    school = School.objects.filter(criterion3 & criterion4).distinct()

    schoolfilter = SchoolFilter(request.GET, queryset=SchoolType.objects.filter(
        school__school_status='AC').distinct())
    schooltypesnav = SchoolType.objects.filter(school__school_status='AC').annotate(
        cats_num=Count('school')).order_by('-cats_num')[:4]
    schoolregionsnav = Region.objects.filter(
        country__city__schooladdress__school__school_status='AC').distinct().annotate(
        region_num=Count('country')).order_by('-region_num')
    citiesnav = City.objects.filter(
        schooladdress__school__school_status='AC').distinct().annotate(
        city_num=Count('schooladdress__school')).order_by('-city_num')[:12]
    countriesnav = Country.objects.filter(
        city__schooladdress__school__school_status='AC').distinct().annotate(
        country_num=Count('city__schooladdress__school')).order_by('-country_num')[:12]

    return render(request, 'schools/school-city.html',
                  {'cities': cities.title().replace('-', ' '), 'cities': city, 'schools': school,
                   'schoolfilter': schoolfilter,
                   'schooltypesnav': schooltypesnav,
                   'schoolregionsnav': schoolregionsnav,
                   'citiesnav': citiesnav,
                   'countriesnav': countriesnav})


class SchoolViewSet(viewsets.ModelViewSet):
    # queryset = School.objects.filter(school_status='AC')
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


def searchschools(request):
    if request.method == "GET":
        searched = request.GET['searched']

        criterion1 = Q(schooladdress__school__school_status='AC')
        #criterion2 = Q(city_name__icontains=cities.replace('-', ' '))
        criterion3 = Q(school_status='AC')
        #criterion4 = Q(address__city__city_name__icontains=cities.replace('-', ' '))
        criterion5 = Q(school_name__icontains=searched)
        criterion6 = Q(schooltype__schooltype_name__icontains=searched)
        criterion7 = Q(address__city__city_name__icontains=searched)
        criterion8 = Q(address__city__country__country_name__icontains=searched)
        criterion9 = Q(address__city__country__region__region_name__icontains=searched)
        #city = City.objects.filter(criterion1 & criterion2).distinct()
        school = School.objects.filter((criterion5 | criterion6 | criterion7 | criterion8 | criterion9) & criterion3)


        #school = School.objects.filter(school_name__icontains=searched, school_status='AC')
        schoolfilter = SchoolFilter(request.GET, queryset=SchoolType.objects.filter(
            school__school_status='AC').distinct())
        schooltypesnav = SchoolType.objects.filter(school__school_status='AC').annotate(
            cats_num=Count('school')).order_by('-cats_num')[:4]
        schoolregionsnav = Region.objects.filter(
            country__city__schooladdress__school__school_status='AC').distinct().annotate(
            region_num=Count('country')).order_by('-region_num')
        citiesnav = City.objects.filter(
            schooladdress__school__school_status='AC').distinct().annotate(
            city_num=Count('schooladdress__school')).order_by('-city_num')[:12]
        countriesnav = Country.objects.filter(
            city__schooladdress__school__school_status='AC').distinct().annotate(
            country_num=Count('city__schooladdress__school')).order_by('-country_num')[:12]
        return render(request, 'schools/search_schools.html', {'searched': searched, 'schools': school,
                   'schoolfilter': schoolfilter,
                   'schooltypesnav': schooltypesnav,
                   'schoolregionsnav': schoolregionsnav,
                   'citiesnav': citiesnav,
                   'countriesnav': countriesnav})
    else:

        schoolfilter = SchoolFilter(request.GET, queryset=SchoolType.objects.filter(
            school__school_status='AC').distinct())
        schooltypesnav = SchoolType.objects.filter(school__school_status='AC').annotate(
            cats_num=Count('school')).order_by('-cats_num')[:4]
        schoolregionsnav = Region.objects.filter(
            country__city__schooladdress__school__school_status='AC').distinct().annotate(
            region_num=Count('country')).order_by('-region_num')
        citiesnav = City.objects.filter(
            schooladdress__school__school_status='AC').distinct().annotate(
            city_num=Count('schooladdress__school')).order_by('-city_num')[:12]
        countriesnav = Country.objects.filter(
            city__schooladdress__school__school_status='AC').distinct().annotate(
            country_num=Count('city__schooladdress__school')).order_by('-country_num')[:12]
        return render(request, 'schools/search_schools.html', {
                   'schoolfilter': schoolfilter,
                   'schooltypesnav': schooltypesnav,
                   'schoolregionsnav': schoolregionsnav,
                   'citiesnav': citiesnav,
                   'countriesnav': countriesnav})


def error_404(request, exception):
    schooltypesnav = SchoolType.objects.filter(school__school_status='AC').annotate(
        cats_num=Count('school')).order_by('-cats_num')[:4]
    schoolregionsnav = Region.objects.filter(
        country__city__schooladdress__school__school_status='AC').distinct().annotate(
        region_num=Count('country')).order_by('-region_num')
    citiesnav = City.objects.filter(
        schooladdress__school__school_status='AC').distinct().annotate(
        city_num=Count('schooladdress__school')).order_by('-city_num')[:12]
    countriesnav = Country.objects.filter(
        city__schooladdress__school__school_status='AC').distinct().annotate(
        country_num=Count('city__schooladdress__school')).order_by('-country_num')[:12]
    return render(request, 'schools/404.html', {
                   'schooltypesnav': schooltypesnav,
                   'schoolregionsnav': schoolregionsnav,
                   'citiesnav': citiesnav,
                   'countriesnav': countriesnav})


def error_400(request, exception):
    schooltypesnav = SchoolType.objects.filter(school__school_status='AC').annotate(
        cats_num=Count('school')).order_by('-cats_num')[:4]
    schoolregionsnav = Region.objects.filter(
        country__city__schooladdress__school__school_status='AC').distinct().annotate(
        region_num=Count('country')).order_by('-region_num')
    citiesnav = City.objects.filter(
        schooladdress__school__school_status='AC').distinct().annotate(
        city_num=Count('schooladdress__school')).order_by('-city_num')[:12]
    countriesnav = Country.objects.filter(
        city__schooladdress__school__school_status='AC').distinct().annotate(
        country_num=Count('city__schooladdress__school')).order_by('-country_num')[:12]
    return render(request, 'schools/400.html', {
                   'schooltypesnav': schooltypesnav,
                   'schoolregionsnav': schoolregionsnav,
                   'citiesnav': citiesnav,
                   'countriesnav': countriesnav})


def error_403(request, exception):
    schooltypesnav = SchoolType.objects.filter(school__school_status='AC').annotate(
        cats_num=Count('school')).order_by('-cats_num')[:4]
    schoolregionsnav = Region.objects.filter(
        country__city__schooladdress__school__school_status='AC').distinct().annotate(
        region_num=Count('country')).order_by('-region_num')
    citiesnav = City.objects.filter(
        schooladdress__school__school_status='AC').distinct().annotate(
        city_num=Count('schooladdress__school')).order_by('-city_num')[:12]
    countriesnav = Country.objects.filter(
        city__schooladdress__school__school_status='AC').distinct().annotate(
        country_num=Count('city__schooladdress__school')).order_by('-country_num')[:12]
    return render(request, 'schools/403.html', {
                   'schooltypesnav': schooltypesnav,
                   'schoolregionsnav': schoolregionsnav,
                   'citiesnav': citiesnav,
                   'countriesnav': countriesnav})


def error_500(request):
    schooltypesnav = SchoolType.objects.filter(school__school_status='AC').annotate(
        cats_num=Count('school')).order_by('-cats_num')[:4]
    schoolregionsnav = Region.objects.filter(
        country__city__schooladdress__school__school_status='AC').distinct().annotate(
        region_num=Count('country')).order_by('-region_num')
    citiesnav = City.objects.filter(
        schooladdress__school__school_status='AC').distinct().annotate(
        city_num=Count('schooladdress__school')).order_by('-city_num')[:12]
    countriesnav = Country.objects.filter(
        city__schooladdress__school__school_status='AC').distinct().annotate(
        country_num=Count('city__schooladdress__school')).order_by('-country_num')[:12]
    return render(request, 'schools/500.html', {
                   'schooltypesnav': schooltypesnav,
                   'schoolregionsnav': schoolregionsnav,
                   'citiesnav': citiesnav,
                   'countriesnav': countriesnav})

