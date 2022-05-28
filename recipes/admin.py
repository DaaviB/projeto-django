from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from tag.models import Tag

from .models import Category, Recipe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


class TagInline(GenericStackedInline):
    model = Tag
    fields = 'name',
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'created_at', 'is_published',)
    list_display_links = ('title', 'created_at',)
    search_fields = (
        'id', 'title', 'slug', 'created_at',
        'description', 'preparation_steps',
    )
    list_filter = (
        'category', 'author', 'created_at',
        'update_at', 'is_published',
    )
    list_per_page = 10
    list_editable = ('is_published',)
    ordering = ('-id',)
    prepopulated_fields = {
        'slug': ('title',)
    }
    inlines = [
        TagInline,
    ]
