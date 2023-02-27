from django.db import models
from django.db.models import CASCADE
from django.utils import timezone

from core.models import User


class DatesModelMixin(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)


class GoalCategory(DatesModelMixin):
    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    class Meta:
        ordering = ['created']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    objects = models.Manager()


class Status(models.IntegerChoices):
    to_do = 1, "К выполнению"
    in_progress = 2, "В процессе"
    done = 3, "Выполнено"
    archived = 4, "Архив"


class Priority(models.IntegerChoices):
    low = 1, "Низкий"
    medium = 2, "Средний"
    high = 3, "Высокий"
    critical = 4, "Критический"


class Goal(DatesModelMixin):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="Название", max_length=255)
    category = models.ForeignKey(GoalCategory, verbose_name="Категория", on_delete=models.CASCADE)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    description = models.CharField(verbose_name="Описание", max_length=300)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    due_date = models.DateTimeField(verbose_name="Дэдлайн")
    status = models.PositiveSmallIntegerField(
        verbose_name="Статус", choices=Status.choices, default=Status.to_do
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name="Приоритет", choices=Priority.choices, default=Priority.medium
    )

    class Meta:
        ordering = ['-priority']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    objects = models.Manager()


class GoalComment(DatesModelMixin):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=250, verbose_name="Комментарий")
    user = models.ForeignKey(User, on_delete=CASCADE, verbose_name="Автор")
    goal = models.ForeignKey(Goal, on_delete=CASCADE, verbose_name="Задача")

    objects = models.Manager()

    class Meta:
        ordering = ['-created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
