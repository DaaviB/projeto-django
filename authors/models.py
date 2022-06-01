from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Profile(models.Model):
    author = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_('Author'))
    bio = models.TextField(default='', blank=True, verbose_name=_('Bio'))

    def __str__(self):
        return self.author.username

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
