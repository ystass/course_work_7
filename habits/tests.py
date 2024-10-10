from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        # Подготовка данных перед каждым тестом
        self.user = User.objects.create(email="admin@admin.com")
        self.habit = Habit.objects.create(
            place="Дом",
            time="2024-10-10T10:56:23Z",
            action="Утренняя зарядка",
            is_pleasant=False,
            frequency_number=1,
            frequency_unit="days",
            reward="чашечка кофе",
            duration="120",
            is_public=True,
            user=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        url = reverse("habits:habits-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_create(self):
        url = reverse("habits:habits-list")
        data = {
            "place": "участок",
            "time": "2024-10-10T20:40:00",
            "action": "подмести дорожки",
            "is_pleasant": False,
            "frequency_number": 1,
            "frequency_unit": "days",
            "reward": "поиграть в мяч",
            "duration": "00:02:00",
            "is_public": True,
            "user": 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_list(self):
        url = reverse("habits:habits-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_update(self):
        url = reverse("habits:habits-detail", args=(self.habit.pk,))
        data = {
            "reward": "посмотреть фильм",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("reward"), "посмотреть фильм")

    def test_public_habit_list(self):
        url = reverse("habits:public")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_delete(self):
        url = reverse("habits:habits-detail", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)
