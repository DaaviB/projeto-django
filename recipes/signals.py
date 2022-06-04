import os

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from .models import Recipe


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        ...


@receiver(pre_delete, sender=Recipe)
def recipe_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()
    delete_cover(old_instance)


@receiver(pre_save, sender=Recipe)
def recipe_cover_update(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()
    is_new_cover = old_instance.cover != instance.cover

    if not old_instance:
        return
    print(is_new_cover)
    if is_new_cover:
        delete_cover(old_instance)
