# your_django_app/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import timedelta


class CustomUser(AbstractUser):
    telegram_id = models.CharField(max_length=100, unique=True, null=True, blank=True)


class Habits(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='related_habits')
    periodicity = models.IntegerField(default=1, validators=[MinValueValidator(1),
                                                             MaxValueValidator(7)])  # Валидатор для периодичности
    reward = models.CharField(max_length=255, blank=True, null=True)
    duration = models.DurationField(
        validators=[MaxValueValidator(timedelta(minutes=2))])  # Валидатор для времени выполнения
    is_public = models.BooleanField(default=False)

    def clean(self):
        # Исключить одновременный выбор связанной привычки и указания вознаграждения
        if self.related_habit and self.reward:
            raise ValidationError("Не может быть указано одновременно и вознаграждение, и связанная привычка.")

        # Привычка может быть связанной только если она является приятной
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")

        # У приятной привычки не может быть вознаграждения или связанной привычки
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")

        # Нельзя выполнять привычку реже, чем 1 раз в 7 дней
        if self.periodicity < 1 or self.periodicity > 7:
            raise ValidationError("Периодичность выполнения привычки должна быть от 1 до 7 дней.")

    def __str__(self):
        return f"{self.action} at {self.time} in {self.place}"

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(periodicity__gte=1, periodicity__lte=7), name='valid_periodicity'),
            models.CheckConstraint(check=models.Q(duration__lte=timedelta(minutes=2)), name='valid_duration')
        ]
