from django.contrib import admin
from .models import City
from .models import Station

# Register your models here.
class CityAdmin(admin.ModelAdmin):
    list_display = ('place_name', 'admin_code1', 'latitude', 'longitude')
    list_filter = ['admin_code1']
    search_fields = ['place_name']

class StationAdmin(admin.ModelAdmin):
    list_display = ('id_code', 'station_name', 'station_state', 'latitude', 'longitude')
    list_filter = ['station_state']
    search_fields = ['station_name', 'id_code']
    
admin.site.register(City, CityAdmin)
admin.site.register(Station, StationAdmin)

