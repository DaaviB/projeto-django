import os
from collections import defaultdict

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from PIL import Image
from tag.models import Tag


class Category(models.Model):
    name = models.CharField(max_length=65, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Recipe(models.Model):
    title = models.CharField(max_length=65, verbose_name=_('Title'))
    description = models.CharField(
        max_length=165, verbose_name=_('Description'))
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField(verbose_name=_('Preparation time'))
    preparation_time_unit = models.CharField(
        max_length=65, verbose_name=_('Preparation time unit'))
    servings = models.IntegerField(verbose_name=_('Servings'))
    servings_unit = models.CharField(
        max_length=65, verbose_name=_('Servings unit'))
    preparation_steps = models.TextField(verbose_name=_('Preparation steps'))
    preparation_steps_is_html = models.BooleanField(
        default=False, verbose_name=_('preparation steps is html'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created_at'))
    update_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Update_at'))
    is_published = models.BooleanField(
        default=False, verbose_name=_('Is_published'))
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d',
        null=True, blank=True, default=None, verbose_name=_('Cover'))  # noqa: E501
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        blank=True, default=None, verbose_name=_('Category')
    )  # noqa: E501
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name=_('Author')
    )
    tags = models.ManyToManyField(
        Tag, blank=True, default='', verbose_name=_('Tags'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipes:recipe", kwargs={"pk": self.id})

    @staticmethod
    def resize_image(image, width=840):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)

        original_width, original_height = image_pillow.size

        if original_width == width:
            image_pillow.close()
            return

        height = round((width * original_height) / original_width)

        new_image = image_pillow.resize((width, height), Image.LANCZOS)

        new_image.save(
            image_full_path,
            optimize=True,
            quality=60,
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        save = super().save(*args, **kwargs)

        if self.cover:
            try:
                self.resize_image(self.cover)
            except FileNotFoundError:
                ...

        return save

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

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
