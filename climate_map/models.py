from django.db import models

# Create your models here.
class City(models.Model):
    postal_code = models.CharField(max_length=8)
    place_name = models.CharField(max_length=50)
    admin_name1 = models.CharField(max_length=50, blank=True, default='')
    admin_code1 = models.CharField(max_length=3, blank=True, default='')
    admin_name2 = models.CharField(max_length=50, blank=True, default='')
    admin_code2 = models.IntegerField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=7, decimal_places=4)
    longitude = models.DecimalField(max_digits=7, decimal_places=4)

    def __str__(self):
    	name = self.place_name + ', ' + self.admin_code1
    	return name


class US_city(models.Model):
    postal_code = models.CharField(max_length=8)
    place_name = models.CharField(max_length=50)
    admin_name1 = models.CharField(max_length=50, blank=True, default='')
    admin_code1 = models.CharField(max_length=3, blank=True, default='')
    admin_name2 = models.CharField(max_length=50, blank=True, default='')
    admin_code2 = models.IntegerField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=7, decimal_places=4)
    longitude = models.DecimalField(max_digits=7, decimal_places=4)

    def __str__(self):
        name = self.place_name + ', ' + self.admin_code1
        return name


class Station(models.Model):
    id_code = models.CharField(max_length=11)
    latitude = models.DecimalField(max_digits=8, decimal_places=4)
    longitude = models.DecimalField(max_digits=8, decimal_places=4)
    station_state = models.CharField(max_length=2)
    station_name = models.CharField(max_length=30)

    def __str__(self):
        name = self.id_code
        return name

