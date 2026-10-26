from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskCrudTests(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title="Test", description="Desc")

    def test_list_shows_task(self):
        """Список содержит созданную задачу"""
        response = self.client.get(reverse("crud:task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test")

    def test_detail_returns_404_for_missing(self):
        """Несуществующая задача даёт 404"""
        response = self.client.get(reverse("crud:task_detail", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_create(self):
        """POST создаёт задачу и редиректит на список"""
        response = self.client.post(reverse("crud:task_create"), {"title": "New"})
        self.assertRedirects(response, reverse("crud:task_list"))
        self.assertTrue(Task.objects.filter(title="New").exists())

    def test_update(self):
        """POST меняет данные задачи"""
        self.client.post(reverse("crud:task_update", args=[self.task.pk]), {"title": "Changed"})
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Changed")

    def test_delete(self):
        """POST удаляет задачу"""
        self.client.post(reverse("crud:task_delete", args=[self.task.pk]))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
