# your_django_app/tests.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Habits


class HabitTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.habit = Habits.objects.create(user=self.user, place="Home", time="08:00:00", action="Exercise", duration="00:02:00")

    def test_create_habit(self):
        response = self.client.post('/habits/', {
            'place': 'Park',
            'time': '07:00:00',
            'action': 'Jogging',
            'duration': '00:01:30'
        })
        self.assertEqual(response.status_code, 201)

    def test_list_habits(self):
        response = self.client.get('/habits/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_update_habit(self):
        response = self.client.put(f'/habits/{self.habit.id}/', {
            'place': 'Gym',
            'time': '09:00:00',
            'action': 'Workout',
            'duration': '00:01:30'
        })
        self.assertEqual(response.status_code, 200)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.place, 'Gym')

    def test_delete_habit(self):
        response = self.client.delete(f'/habits/{self.habit.id}/')
        self.assertEqual(response.status_code, 204)
