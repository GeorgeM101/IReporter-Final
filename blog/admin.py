from django.contrib import admin

# Register your models here.
from .models import Search, Video
admin.site.register(Video)
admin.site.register(Search)
