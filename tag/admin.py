from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class TagAdmim(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug'
    search_fields = 'id', 'name', 'slug'
    list_display_links = 'id', 'slug'
    list_editable = 'name',
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('name',),
    }
