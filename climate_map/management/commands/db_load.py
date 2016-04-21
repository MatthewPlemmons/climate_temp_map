"""
	Command line script to read in city locations for sqlite database.
"""

import csv
import logging
from django.core.management.base import BaseCommand, CommandError
from climate_map.models import City

class Command(BaseCommand):	
	
	def handle(self, *args, **options):
		filename = 'US.txt'

		# This variable keeps track of the number of rows
		# the csv reader has read through.
		i = 0
		with open(filename) as f:
			reader = csv.reader(f, delimiter='\t')
			for row in reader:
				city = City()
				city.postal_code = row[1]
				city.place_name = row[2]
				city.admin_name1 = row[3]
				city.admin_code1 = row[4]
				city.admin_name2 = row[5]
				city.admin_code2 = row[6]
				city.latitude = row[9]
				city.longitude = row[10]

				if 'FPO' in row[2]:
					continue
				elif 'APO' in row[2]:
					continue
				else:
					try:
						city.save()
					except Exception as e:
						logging.exception('Error saving to database table on row number "%s"' % i)
						logging.exception('Error: "%s"' % e)

				# Increase i by one to represent the next row number in the file
				i = i + 1

		self.stdout.write(self.style.SUCCESS('Number of rows saved to database table: "%s"' % i))


