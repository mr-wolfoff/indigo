from django.core.validators import FileExtensionValidator
from django.db import models


class Video(models.Model):
    article = models.ForeignKey(
        to='webapp.Article',
        related_name='videos',
        verbose_name='Статья',
        on_delete=models.CASCADE
    )
    source = models.FileField(
        upload_to='videos_uploaded',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(
        allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv']
        )]
    )
