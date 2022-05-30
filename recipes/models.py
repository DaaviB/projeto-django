from collections import defaultdict

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from tag.models import Tag


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d',
        null=True, blank=True, default=None)  # noqa: E501
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        blank=True, default=None,
    )  # noqa: E501
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipes:recipe", kwargs={"pk": self.id})

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        return super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title,
        ).first()

        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Found recipe with th same title',
                )

        if error_messages:
            raise ValidationError(error_messages)
