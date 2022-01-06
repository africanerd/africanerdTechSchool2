from django.urls import path
from django.conf.urls import url, include
from .api import SchoolViewSet
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'schools-view', views.SchoolViewSet)


app_name = 'schools'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('schoolview/', views.SchoolIndexView.as_view(), name='school'),
    path('schooldetail/<int:pk>/', views.SchoolDetailView.as_view(), name='school_detail'),
    path('schoolview2/', views.SchoolIndexView2.as_view(), name='school2'),
    path('schooldetail2/<slug:slug>/', views.SchoolDetailView2.as_view(), name='school_detail2'),
    #path('schooldetail2/<int:pk>/', views.SchoolDetailView2.as_view(), name='school_detail2'),
    path('category/<str:cats>/', views.categoryview, name='school_category'),
    path('region/<str:regs>/', views.regionview, name='school_region'),
    path('city/<str:cities>/', views.cityview, name='school_city'),
    path('country/<str:cnts>/', views.countryview, name='school_country'),
    url('^api/', include(router.urls)),
    path('search_schools/', views.searchschools, name='schools_search')
    # url(r'^schooltypes$', SchoolTypeApi.as_view()),
    # url(r'^schooladdress$', SchoolAddressApi.as_view())
]
