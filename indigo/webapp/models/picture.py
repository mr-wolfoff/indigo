from django.db import models


class Picture(models.Model):
    article = models.ForeignKey(
        to='webapp.Article',
        related_name='pictures',
        verbose_name='Статья',
        on_delete=models.CASCADE
    )
    source = models.FileField(
        blank=True,
        null=True,
        upload_to='pictures',
        verbose_name='Изображение')
