from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.shortcuts import render
from django.db.models import Q
from .models import Region, Continent, SchoolType, SchoolImage, School, SchoolAddress, City
from .schoolfilters import SchoolFilter


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
        return SchoolType.objects.all()


class SchoolDetailView(generic.DetailView):
    model = SchoolType
    template_name = 'schools/schooldetail.html'

    def get_queryset(self):
        return SchoolType.objects.all()


class SchoolIndexView2(generic.ListView):
    model = School
    queryset = School.objects.filter(school_status='AC')
    template_name = 'schools/schoolindex2.html'

    # context_object_name = 'allschools'

    # schoolFilter = SchoolFilter()

    # def get_queryset(self):
    #     return School.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['schools'] = School.objects.filter()
        # schools = School.objects.filter()
        context['schoolfilter'] = SchoolFilter(self.request.GET, queryset=self.get_queryset())

        return context


class SchoolDetailView2(generic.DetailView):
    model = School
    template_name = 'schools/schooldetail2.html'

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
        # context["category"] = "MISC"
        # context['cities'] = City.objects.filter(schooladdress=city)

        return context


def categoryview(request, cats):
    criterion1 = Q(school__school_status='AC')
    criterion2 = Q(schooltype_name__icontains=cats.replace('-', ' '))
    criterion3 = Q(school_status='AC')
    criterion4 = Q(schooltype__schooltype_name__icontains=cats.replace('-', ' '))
    schooltype = SchoolType.objects.filter(criterion1 & criterion2).distinct()
    school = School.objects.filter(criterion3 & criterion4).distinct()
    return render(request, 'schools/categories.html',
                  {'cats': cats.title().replace('-', ' '), 'schooltypes': schooltype, 'schools': school})
