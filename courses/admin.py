from django.contrib import admin

from .models import Announcement  # import your model

admin.site.register(Announcement)  # register the model
