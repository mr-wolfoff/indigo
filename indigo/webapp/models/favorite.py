from django.contrib.auth import get_user_model
from django.db import models

from webapp.models import Article


class Favorite(models.Model):
    user = models.ForeignKey(
        to=get_user_model(),
        related_name='favorite_articles',
        verbose_name='Избранное',
        null=False,
        on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        to=Article,
        related_name='favorite_users',
        verbose_name='Избранное',
        null=False,
        on_delete=models.CASCADE
    )
    note = models.CharField(
        max_length=30,
        verbose_name='Текстовая заметка',
        null=False,
        blank=True
    )

    class Meta:
        verbose_name = 'Избранная запись',
        verbose_name_plural = 'Избранные записи'
