# your_django_app/serializers.py

from rest_framework import serializers
from .models import Habits, CustomUser


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habits
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
