from django.db import models
from django.utils import timezone
from africanerdSchool.utils import unique_slug_generator
from django.contrib import admin
import datetime
from django.db.models.signals import pre_save
from django.utils.text import slugify


class Continent(models.Model):
    continent_name = models.CharField(max_length=200, default='Africa')
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

    class Meta:
        verbose_name_plural = "Region"
        ordering = ['region_name']

    def __str__(self):
        return self.region_name


class Country(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    country_name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['country_name']

    def __str__(self):
        return self.country_name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Cities"
        ordering = ['city_name']

    def __str__(self):
        return self.city_name


class SchoolAddress(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    schooladdress_street = models.CharField(max_length=200)
    schooladdress_pob = models.CharField(max_length=200)
    schooladdress_stateprovince = models.CharField(max_length=200)
    schooladdress_postalcode = models.CharField(max_length=200)

    def __str__(self):
        return self.schooladdress_street


class SchoolType(models.Model):
    schooltype_name = models.CharField(max_length=200)
    schooltype_desc = models.TextField(max_length=200, blank=True, default='Enter Text', null=True)
    schooltype_color = models.CharField(max_length=200, blank=True, default='Enter Text', null=True)

    def __str__(self):
        return self.schooltype_name


class SchoolImage(models.Model):
    school_imgname = models.CharField(max_length=200, default='School')
    school_imgdesc = models.CharField(max_length=200, blank=True, default='School', null=True)
    school_imgsourcename = models.CharField(max_length=200, blank=True, default='School', null=True)
    school_imgurlmain = models.ImageField(upload_to='img/school/%Y/%m/%d/', blank=True)


    def __str__(self):
        return self.school_imgname


class School(models.Model):
    ACTIVE = 'AC'
    INACTIVE = 'IN'
    SCHOOL_STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]

    schooltype = models.ForeignKey(SchoolType, on_delete=models.CASCADE, blank=True, null=True)
    address = models.ManyToManyField(SchoolAddress)
    school_name = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)
    #slug = models.SlugField(max_length=250, null=True, blank=True)
    image = models.ForeignKey(SchoolImage, on_delete=models.CASCADE, blank=True, null=True)
    school_program = models.CharField(max_length=200)
    school_programdesc = models.TextField(null=True, blank=True)
    school_url = models.URLField(max_length=200)
    school_pub_date = models.DateTimeField('date published')
    school_status = models.CharField(max_length=2, default=INACTIVE, choices=SCHOOL_STATUS_CHOICES, blank=True,
                                     null=True)

    def __str__(self):
        return self.school_name

    class Meta:
        ordering = ['-school_pub_date']

    @admin.display(
        boolean=True,
        ordering='school_pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.school_pub_date <= now


def schoolslug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

# @receiver(pre_save, sender=School)
# def pre_save_receiver(sender, instance, *args, **kwargs):
#    if not instance.school_slug:
#        instance.school_slug = unique_slug_generator(instance)

pre_save.connect(schoolslug_generator, sender=School)