from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Model


class Author(Model):
    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')

    name = models.TextField(blank=False, max_length=150)
    description = models.TextField(blank=True, null=False, max_length=512)

    portrait_picture = models.ImageField(upload_to='authors', blank=True)

    promote = models.BooleanField(default=False, help_text=_('Promote on the main page'))

    def __str__(self):
        return self.name
