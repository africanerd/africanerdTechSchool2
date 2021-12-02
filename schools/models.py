from django.db import models
from django.utils import timezone
from django.contrib import admin
import datetime


class Continent(models.Model):
    continent_name = models.CharField(max_length=200)
    continent_pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.continent_name

    @admin.display(
        boolean=True,
        ordering='continent_pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.continent_pub_date <= now


class Region(models.Model):
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    region_name = models.CharField(max_length=200)

    def __str__(self):
        return self.region_name


# class Country(models.Model):
#     region = models.ForeignKey(Region, on_delete=models.CASCADE)
#     country_name = models.CharField(max_length=200)
#
#     def __str__(self):
#         return self.country_name
#

# class Location(models.Model):
#     location_country = models.CharField(max_length=200)
#     location_region = models.CharField(max_length=200)
#     location_city = models.CharField(max_length=200)
#     location_pub_date = models.DateTimeField('date published')
#
#     def __str__(self):
#         return self.location_country
#
#     @admin.display(
#         boolean=True,
#         ordering='pub_date',
#         description='Published recently?',
#     )
#     def was_published_recently(self):
#         now = timezone.now()
#         return now - datetime.timedelta(days=1) <= self.pub_date <= now
#
#
# class School(models.Model):
#     location = models.ForeignKey(Location, on_delete=models.CASCADE)
#     school_name = models.CharField(max_length=200)
#     school_img = models.ImageField(upload_to='img/school/%Y/%m/%d/', blank=True)
#     school_tech_depart_name = models.CharField(max_length=200)
#     school_tech_depart_desc = models.TextField(null=True, blank=True)
#     school_tech_address = models.CharField(null=True, blank=True)
#     school_tech_depart_url = models.URLField(max_length=200)
#     school_pub_date = models.DateTimeField('date published')
#
#     def __str__(self):
#         return self.school_name
#
