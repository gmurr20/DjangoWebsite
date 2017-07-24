from __future__ import unicode_literals

from django.db import models

import os
# Create your models here.

class Company(models.Model):
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    description = models.TextField()
    link = models.CharField(max_length=200)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    photo = models.ImageField(max_length=500, upload_to=os.path.join(BASE_DIR, 'myApp/static/'))
    photoPath = models.CharField(blank=True, max_length=500)
    def __str__(self):
        return self.company

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.CharField(max_length=200)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    photo = models.ImageField(max_length=500, upload_to=os.path.join(BASE_DIR, 'myApp/static/'))
    photoPath = models.CharField(blank=True, max_length=500)
    def __str__(self):
        return self.title

class Photo(models.Model):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    title = models.CharField(max_length=100)
    photo = models.ImageField(max_length=500, upload_to=os.path.join(BASE_DIR, 'myApp/static/uploadedImages/'))
    latitude = models.DecimalField(decimal_places=2, max_digits=10)
    longitude = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField()
    def __str__(self):
        return self.title

class Blog(models.Model):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(max_length=500, upload_to=os.path.join(BASE_DIR, 'myApp/static/blogPhotos/'))
    description = models.TextField()
    section1Title = models.CharField(max_length=100)
    section1Content = models.TextField()
    section2Title = models.CharField(max_length=100)
    section2Content = models.TextField()
    section3Title = models.CharField(max_length=100)
    section3Content = models.TextField()

    def __str__(self):
        return self.title

