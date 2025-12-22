from django.contrib import admin
from .models import blogg, comment, profile


# Register your models here.


@admin.register(blogg)
class adminblogg(admin.ModelAdmin):
    list_display = ['id', 'name', 'title', 'brief', 'date', 'dtn','link', 'user']

@admin.register(comment)
class admincomment(admin.ModelAdmin):
    list_display = ['id', 'commentt', 'usr', 'content', 'dat']


@admin.register(profile)
class adminprofile(admin.ModelAdmin):
    list_display = ['id', 'profile_id', 'dob', 'dp']
