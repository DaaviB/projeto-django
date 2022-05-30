from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = 'id', 'author', 'bio'
    list_display_links = 'id', 'author',
    ordering = '-id',
