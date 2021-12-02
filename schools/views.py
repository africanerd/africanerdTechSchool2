from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Region, Continent


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

