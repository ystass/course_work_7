from datetime import timedelta

from rest_framework.serializers import ValidationError


class RewardValidator:
    """
    Исключает одновременный выбор связанной привычки и указания вознаграждения
    """
    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        tmp_val1 = dict(value).get(self.field1)
        tmp_val2 = dict(value).get(self.field2)
        if tmp_val1 and tmp_val2:
            raise ValidationError(
                "Нельзя одновременный выбрать связанную привычку и указания указать вознаграждение (укажите только одно поле)"
            )


class RelatedHabitValidator:
    """
    Проверяет что связанные привычки могут только приятными
    """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val:
            if not tmp_val.is_pleasant:
                raise ValidationError(
                    "Связанная привычка может быть только приятной привычкой (с полем is_pleasant=True)"
                )


class DurationTimeValidator:
    """
    Проверяет что время выполнения не больше 120 секунд
    """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        print(tmp_val)
        if tmp_val is not None and tmp_val > timedelta(seconds=120):
            raise ValidationError("Время выполнения должно быть не больше 120 секунд")


class PleasantHabitValidator:
    """
    Проверяет что у приятной привычки не может быть вознаграждения или связанной привычки
    """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val:
            our_value = dict(value)
            if (
                our_value.get("reward") is not None
                or our_value.get("related_habit") is not None
            ):
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки"
                )


class RegularityValidator:
    """
    Проверяет что нельзя выполнять привычку реже, чем 1 раз в 7 дней
    """
    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        frequency_in_days = 0
        num = dict(value).get(self.field1)
        unit = dict(value).get(self.field2)

        if num:
            if unit == "minutes":
                frequency_in_days = num / (60 * 24)  # перевод в дни (если указаны минуты)
            elif unit == "hours":
                frequency_in_days = num / 24  # перевод в дни (если указаны часы)
            elif unit == "days":
                frequency_in_days = num

        if frequency_in_days > 7:
            raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней")
