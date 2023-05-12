from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Тег'
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
        return self.name
