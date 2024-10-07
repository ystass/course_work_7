from django.conf import settings
from django.db import models

NULLABLE = {"null": True, "blank": True}


class Habit(models.Model):
    FREQUENCY_UNITS = [
        ("minutes", "минуты"),
        ("hours", "часы"),
        ("days", "дни"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Создатель привычки",
        **NULLABLE,
    )
    place = models.CharField(max_length=200, verbose_name="Место, в котором необходимо выполнять привычку")
    time = models.DateTimeField(verbose_name="Время, когда необходимо выполнять привычку")
    action = models.CharField(max_length=200, verbose_name="Действие, которое представляет собой привычка")
    is_pleasant = models.BooleanField(verbose_name="Признак приятной привычки")
    related_habit = models.ForeignKey(
        "self", on_delete=models.SET_NULL, **NULLABLE, verbose_name="Связанная привычка"
    )  # важно указывать для полезных привычек, но не для приятных
    frequency_number = models.PositiveIntegerField(verbose_name="Периодичность выполнения привычки для напоминания")
    frequency_unit = models.CharField(
        max_length=10,
        choices=FREQUENCY_UNITS,  # выбор периодичности
        default="days",  # по умолчанию в днях
        verbose_name="Единицы измерения",
    )
    reward = models.CharField(max_length=200, verbose_name="Вознаграждение", **NULLABLE)
    duration = models.DurationField(verbose_name="Время, которое предположительно потратит пользователь на выполнение привычки")
    is_public = models.BooleanField(default=True, verbose_name="Признак публичности")

    def __str__(self):
        return f"{self.user} - {self.action}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
