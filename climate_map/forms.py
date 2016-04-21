from django import forms
from .models import City, Station

class CityForm(forms.Form):
    city_location = forms.CharField(label='', max_length=75)

    class Meta:
        model = City
