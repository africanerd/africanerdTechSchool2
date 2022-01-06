from .models import Continent, Region, Country, City, SchoolAddress, School, SchoolType, SchoolImage
from django.contrib import admin


class RegionInline(admin.TabularInline):
    model = Region
    extra = 1


class CountryInline(admin.TabularInline):
    model = Country
    extra = 0


class CityInline(admin.TabularInline):
    model = City
    extra = 0


class SchoolAddressInline(admin.TabularInline):
    model = SchoolAddress
    extra = 0


class SchoolInline(admin.TabularInline):
    model = School
    extra = 0


class SchoolTypeInline(admin.TabularInline):
    model = SchoolType
    extra = 0


class ContinentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['continent_name']}),
        ('Date information', {'fields': ['continent_pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [RegionInline]
    list_display = ('continent_name', 'continent_pub_date', 'was_published_recently')
    list_filter = ['continent_pub_date']
    search_fields = ['continent_name']


admin.site.register(Continent, ContinentAdmin)


class RegionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['region_name', 'region_desc', 'region_icon']}),
    ]
    inlines = [CountryInline]
    list_display = ('region_name', 'region_desc', 'region_icon')
    search_fields = ['region_name']


admin.site.register(Region, RegionAdmin)


class CountryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['country_name', 'country_flagcode']}),
    ]
    inlines = [CityInline]
    list_display = ('country_name', 'country_flagcode')
    search_fields = ['country_name']


admin.site.register(Country, CountryAdmin)


class CityAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,    {'fields': ['city_name']}),
    ]
    inlines = [SchoolAddressInline]
    list_display = ('city_name', 'country')
    search_fields = ['city_name']
    list_filter = ['city_name', 'country']


admin.site.register(City, CityAdmin)


admin.site.register(SchoolAddress)


class SchoolTypeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,    {'fields': ['schooltype_name', 'schooltype_desc', 'schooltype_icon', 'schooltype_color']}),
    ]
    inlines = [SchoolInline]
    list_display = ('schooltype_name', 'schooltype_desc', 'schooltype_icon', 'schooltype_color')
    search_fields = ['schooltype_name']


admin.site.register(SchoolType, SchoolTypeAdmin)


class SchoolAdmin(admin.ModelAdmin):
    search_fields = ['school_name',]
    list_display = ('school_name', 'school_status', 'schooltype')
    list_filter = ['school_status', 'schooltype']


admin.site.register(School, SchoolAdmin)

admin.site.register(SchoolImage)

