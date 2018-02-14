from django.contrib import admin

# Register your models here.
from feeds.models import UserProfile, Feeds

admin.site.register(Feeds)
admin.site.register(UserProfile)
