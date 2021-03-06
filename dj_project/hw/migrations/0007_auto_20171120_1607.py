# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-20 16:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hw', '0006_auto_20171023_1349'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ('-start_date',)},
        ),
        migrations.AlterModelOptions(
            name='hotel',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='traveler',
            options={'ordering': ('last_name', 'first_name')},
        ),
        migrations.AlterField(
            model_name='hotel',
            name='photo',
            field=models.ImageField(blank=True, default='hotel_avats/default.png', upload_to='hotel_avats/'),
        ),
        migrations.AlterField(
            model_name='traveler',
            name='photo',
            field=models.ImageField(blank=True, default='trav_avats/default.png', upload_to='trav_avats/'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='features',
            field=models.ManyToManyField(blank=True, to='hw.HotelFeature'),
        ),
    ]
