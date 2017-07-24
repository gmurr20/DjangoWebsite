# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-24 00:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0005_auto_20170416_2313'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
                ('image', models.ImageField(max_length=500, upload_to='/Users/Gmurr/IdeaProjects/CS242/Final0/myApp/static/blogPhotos')),
                ('content', models.TextField()),
            ],
        ),
    ]