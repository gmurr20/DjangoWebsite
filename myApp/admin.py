from django.contrib import admin

from models import Company
from models import Project
from models import Photo
from models import Blog
# Register your models here.

admin.site.register(Company)
admin.site.register(Project)
admin.site.register(Photo)
admin.site.register(Blog)