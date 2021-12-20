from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'schools'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('schoolview/', views.SchoolIndexView.as_view(), name='school'),
    path('schooldetail/<int:pk>/', views.SchoolDetailView.as_view(), name='school_detail'),
    path('schoolview2/', views.SchoolIndexView2.as_view(), name='school2'),
    path('schooldetail2/<slug:slug>/', views.SchoolDetailView2.as_view(), name='school_detail2'),
    #path('schooldetail2/<int:pk>/', views.SchoolDetailView2.as_view(), name='school_detail2'),
    path('category/<str:cats>/', views.categoryview, name='school_category')
]
