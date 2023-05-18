from django.contrib.auth import get_user_model
from django.db import models


class Comment(models.Model):
    article = models.ForeignKey(
        'webapp.Article',
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Статья',
    )
    text = models.TextField(
        max_length=400,
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        to=get_user_model(),
        null=True,
        blank=False,
        default='No name',
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата и время обновления"
    )

    def __str__(self):
        return f"{self.author} - {self.text[:25]}"
