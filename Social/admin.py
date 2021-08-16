from django.contrib import admin
from django.contrib.admin.sites import site
from Social.models import Posts, Profile

admin.site.register(Posts)
admin.site.register(Profile)