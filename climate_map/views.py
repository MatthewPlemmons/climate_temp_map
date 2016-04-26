from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import City, Station
from django.views import generic
from decimal import *

import pandas as pd

import matplotlib.pyplot as plt
import matplotlib

import plotly.tools as tls
import plotly.plotly as py
import plotly.graph_objs as go

#import matplotlib.pyplot as plt
#import matplotlib

import operator
import os
import json

import pdb

from .forms import CityForm



def index(request):

    if request.method == 'POST':

        # create a form instance and populate it with data from the requst
        form = CityForm(request.POST)

        # check whether it's valid
        if form.is_valid():

            # process the data in form.cleaned_data
            cleaned_data = form.cleaned_data

            cities_q = City.objects.filter(postal_code=cleaned_data['city_location'])
            return render(request, 'index/index.html', {'cities_query': city_q[0].__str__()})

    # if request.content_type == 'application/json':
    #   return render(request)

    else:
        form = CityForm()

    k = os.environ['PRIVATE_KEY']
    return render(request, 'index/index.html', {'city_form': form, 'key': k})


"""
Takes user input and uses it to search the database for a city
by name or zipcode.
"""
def search(request):
    city_list = []
    if request.method == "GET":
        if request.GET.get('geo'):
            geo = request.GET.get('geo')

            # Filters cities based on zipcode or name, limiting the results returned to 10.
            city_locations_zip = City.objects.filter(postal_code__icontains=geo)[:10]
            city_locations_name = City.objects.filter(place_name__icontains=geo)[:10]

            # Iterate over both QuerySets and add any data within
            # to city_list
            for e in city_locations_zip:
                city_list += [{
                    'postal_code': e.postal_code,
                    'place_name': e.place_name,
                    'admin_name1': e.admin_name1,
                    'admin_code1': e.admin_code1,
                    'admin_name2': e.admin_name2,
                    'admin_code2': e.admin_code2,
                    'latitude': float(e.latitude),
                    'longitude': float(e.longitude),
                }]

            for e in city_locations_name:
                city_list += [{
                    'postal_code': e.postal_code,
                    'place_name': e.place_name,
                    'admin_name1': e.admin_name1,
                    'admin_code1': e.admin_code1,
                    'admin_name2': e.admin_name2,
                    'admin_code2': e.admin_code2,
                    'latitude': float(e.latitude),
                    'longitude': float(e.longitude),
                }]

            json_data = (json.dumps(city_list, sort_keys=True, indent=4))
            #print(json_data)
            return HttpResponse(json_data, content_type='application/json') 



def temperature_data(station_id):

    # Get dataframe of weather data
    df = download_station_data(station_id[0]['id_code'])

    # Process the dataframe
    yr_avg = process_weather_data(df)

    # Getting rid of the beginning and ending year, as they only
    # contained partial weather data.
    yr_avg = yr_avg.iloc[1:-1]

    earliest_year = yr_avg.index[0].year
    most_recent_year = yr_avg.index[len(yr_avg.index) - 1].year

    if most_recent_year <= 2012:

        # Call .dly download function
        df = download_station_data(station_id[1]['id_code'])

        # Check the last year on the datetimeindex
        # if it's > 2012, take the last year on the previous df
        # and index into the new df starting there.
        next_station_df = process_weather_data(df)
        if next_station_df.index[len(next_station_df.index) - 1].year > 2012:

            # Getting a dataframe containing only the years needed.
            df_recent = next_station_df[str(most_recent_year):]
            df_recent = df_recent.iloc[1:-1]
            #yr_avg = pd.concat([yr_avg, yr_avg_recent])
            if earliest_year >= 1940: 
                if next_station_df.index[0].year < 1940:
                    df_earlier = next_station_df[:str(earliest_year)]
                    df_earlier = df_earlier.iloc[1:-1]
                    yr_avg = pd.concat([df_earlier, yr_avg, df_recent])
            yr_avg = pd.concat([yr_avg, df_recent])


    trace_hi = go.Scatter(
        x = yr_avg.index,
        y = yr_avg[0],
        name = 'Highs'
    )
    trace_lo = go.Scatter(
        x = yr_avg.index,
        y = yr_avg[1],
        name = 'Lows'
    )
    trace_avg = go.Scatter(
        x = yr_avg.index,
        y = yr_avg[2],
        name = 'Average'
    )
    

    data = [trace_hi, trace_lo, trace_avg]

    url = py.plot(data, filename='pandas-temperature')

    url = url + "/highs-lows-average.json"
    return url




"""
Finds the weather stations nearest to the city.
"""
def station(request):
    station_list = []

    if request.method == "GET":

        # Make sure there is a lat and lng variable to retrieve.
        if request.GET.get('lat') and request.GET.get('lng'):

            # Save the lat and lng values as floats in order to
            # do arithmetic on them later.
            lat = float(request.GET.get('lat'))
            lng = float(request.GET.get('lng'))

            # Get the stations closest to the target city.  Arbitrarily searching
            # a region that's within + and - .80 of the city's lat and lng.  I think
            # this will retrieve stations within around an 80 mile square perimeter
            # of the city.
            nearest_stations = Station.objects.filter(
                latitude__gte=lat - .80,
                latitude__lte=lat + .80, 
                longitude__gte=lng - .80,
                longitude__lte=lng + .80,
                )

            for e in nearest_stations:

                """
                Getting the absolute value of the difference between
                the city's lat & lng and the station's lat & lng and then
                adding them together gives a general idea about the distance
                between them.  Higher numbers mean the station and the city are
                further apart.  Lower numbers, closer together.
                """
                lat_dist = abs(lat - float(e.latitude)) 
                lng_dist = abs(lng - (float(e.longitude)))

                total_dist = lat_dist + lng_dist

                station_list += [{
                    'id_code': e.id_code,
                    'latitude': float(e.latitude),
                    'longitude': float(e.longitude),
                    'station_state': e.station_state,
                    'station_name': e.station_name,
                    'total_dist': total_dist
                }]

    # Small function to use for the 'key' attribute of sorted().
    def get_dist(station):
        return station['total_dist']

    # Sort the stations based on distance to the target city.
    station_list_sorted = sorted(station_list, key=get_dist)

    url = temperature_data(station_list_sorted)

    json_data = (json.dumps(url, sort_keys=True, indent=4))
    print(json_data)
    response = HttpResponse(json_data, content_type='application/json')
    return response


def all_stations(request):
    station_list = []
    all_stations = Station.objects.all()

    for e in all_stations:
        # uniq_id = e.station_state

        station_list += [{
            'id_code': e.id_code,
            'latitude': float(e.latitude),
            'longitude': float(e.longitude),
            'station_state': e.station_state,
            'station_name': e.station_name,
        }]

    json_data = (json.dumps(station_list, sort_keys=True, indent=4))
    response = HttpResponse(json_data, content_type='application/json')
    return response


def download_station_data(station_id):

    #station_id = 'USC00167344'
    
    station_url = "ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/all/" + station_id + ".dly"

    # Changing position 1 and 2 ( values being 4 and 2 (4 being the year, and 2 being the month))
    # Combining them to a width of 6, instead of two widths of 4 and 2.
    widths = [11, 4, 2, 4, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 

1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 

1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 

1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1]

    # starts at 1 to exclude the station ID from the data
    # 1, 2, 3 are the year, month and measurment type.
    cols = [1, 2, 3, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64,
         68, 72, 76, 80, 84, 88, 92, 96, 100, 104, 108, 112, 116, 120, 124]

    #cols = [1, 2, 3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63,
    #    67, 71, 75, 79, 83, 87, 91, 95, 99, 103, 107, 111, 115, 119, 123]

    names = ['year', 'month', 'data_type', 1, 2, 3, 4, 5, 6, 7, 8, 9,
        10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

    df = pd.read_fwf(station_url, widths=widths, usecols=cols, 
        header=None, names=names, parse_dates=[['year', 'month']], index_col=0, na_values='-9999')

    return df


def process_weather_data(df):

    # Selects just the TMAX and TMIN rows.
    df1 = df.loc[df['data_type'].isin(['TMAX'])]
    df2 = df.loc[df['data_type'].isin(['TMIN'])]

    # Selects only temperature data, ignoring the column 'data_type'. 
    # Converts all temperature recordings to Fahrenheit.
    dfmax = df1.iloc[:, 1:]
    dfmax = ((dfmax / 10)) #* 1.8) + 32

    dfmin = df2.iloc[:, 1:]
    dfmin = ((dfmin / 10)) #* 1.8) + 32

    max_avg = dfmax.mean(axis=1)
    min_avg = dfmin.mean(axis=1)

    maxmin_avg = pd.concat([max_avg, min_avg], axis=1)

    avg_temps = pd.concat([max_avg, min_avg, maxmin_avg.mean(axis=1)], axis=1, keys=[0, 1, 2])

    #if avg_temps.index[0].is_year_start:

    #if avg_temps.index[len(avg_temps.index) - 1].is_year_start:

    # Gets the yearly average of the data
    g = pd.TimeGrouper('AS')
    yr_avg = avg_temps.groupby(g).mean()

    return yr_avg

