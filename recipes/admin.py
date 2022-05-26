from django.contrib import admin

from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):

    ...


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


admin.site.register(Category, CategoryAdmin)
