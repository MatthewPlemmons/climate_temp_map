"""
	Command line script to read in US weather stations for sqlite database.
"""

import logging
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from climate_map.models import Station

class Command(BaseCommand):	
	
	def handle(self, *args, **options):
		filename = 'primary_US_stations.txt'

		# Using pandas' read_fwf function to parse fixed width
		# data files.  The columnwidths name is a list of tuples
		# specifying beginning and ending of each column in the file.  
		columnwidths = [(0,11), (12,20), (21,30), (31,37), (38,40), (41,71), (72,75), (76,79), (80,85)]
		df = pd.read_fwf(filename, colspecs=columnwidths, header=None)

		stations = [
			Station(
				id_code = row[1],
				latitude = row[2],
				longitude = row[3],
				station_state = row[5],
				station_name = row[6],
			) 
			for row in df.itertuples()
		]

		try:
			Station.objects.bulk_create(stations)
		except Exception as e:
			logging.exception('Error loading data into table: "%s"' % e)
		
