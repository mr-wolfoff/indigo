from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models import TextChoices

from webapp.managers import ArticleManager


class StatusChoice(TextChoices):
    ACTIVE = 'ACTIVE', 'Активна'
    NOT_ACTIVE = 'NOT_ACTIVE', 'Неактивна'


class Article(models.Model):
    status = models.CharField(
        verbose_name='Статус',
        choices=StatusChoice.choices,
        max_length=20,
        default=StatusChoice.ACTIVE)
    title = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name="Заголовок"
    )
    text = models.TextField(
        max_length=3000,
        null=False,
        blank=False,
        verbose_name="Текст"
    )
    author = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name="Автор"
    )
    is_deleted = models.BooleanField(
        verbose_name='удалено',
        null=False,
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата и время обновления"
    )
    deleted_at = models.DateTimeField(
        verbose_name='Дата и время удаления',
        null=True,
        default=None
    )
    tags = models.ManyToManyField(
        to='webapp.Tag',
        related_name='articles',
        blank=True
    )

    users = models.ManyToManyField(
        through='webapp.Favorite',
        to=User,
        related_name='articles'
    )

    def __str__(self):
        return f"{self.author} - {self.title}"

    objects = ArticleManager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    @property
    def as_dict(self):
        return {
            'id': self.pk,
            'text': self.text,
            'title': self.title,
            'status': self.status,
            'author': self.author
        }

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

