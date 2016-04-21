# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-10 19:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('climate_map', '0001_initial'), ('climate_map', '0002_auto_20160208_1638'), ('climate_map', '0003_auto_20160209_0246'), ('climate_map', '0004_auto_20160209_1949'), ('climate_map', '0005_auto_20160209_2031')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postal_code', models.CharField(max_length=8)),
                ('place_name', models.CharField(max_length=50)),
                ('admin_name1', models.CharField(blank=True, default='', max_length=50)),
                ('admin_code1', models.CharField(blank=True, default='', max_length=3)),
                ('admin_name2', models.CharField(blank=True, default='', max_length=50)),
                ('admin_code2', models.IntegerField(blank=True, null=True)),
                ('latitude', models.DecimalField(decimal_places=4, max_digits=7)),
                ('longitude', models.DecimalField(decimal_places=4, max_digits=7)),
            ],
        ),
    ]