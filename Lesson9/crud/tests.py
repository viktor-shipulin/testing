from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Task


class TaskModelTests(TestCase):
    def test_str_returns_title(self):
        """__str__ возвращает название задачи"""
        task = Task.objects.create(title="Купить хлеб")
        self.assertEqual(str(task), "Купить хлеб")

    def test_done_is_false_by_default(self):
        """Новая задача по умолчанию не выполнена"""
        task = Task.objects.create(title="Test")
        self.assertFalse(task.done)

    def test_description_can_be_blank(self):
        """Описание необязательно и по умолчанию пустое"""
        task = Task.objects.create(title="Test")
        self.assertEqual(task.description, "")

    def test_ordering_newest_first(self):
        """Задачи сортируются от новых к старым"""
        old = Task.objects.create(title="Old")
        new = Task.objects.create(title="New")
        Task.objects.filter(pk=old.pk).update(created_at=timezone.now() - timedelta(days=1))
        self.assertEqual(list(Task.objects.all()), [new, old])


class TaskListViewTests(TestCase):
    def test_list_status_and_template(self):
        """Страница списка открывается и использует нужный шаблон"""
        response = self.client.get(reverse("crud:task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "crud/task_list.html")

    def test_list_empty_message(self):
        """Если задач нет, показывается сообщение «Задач пока нет»"""
        response = self.client.get(reverse("crud:task_list"))
        self.assertContains(response, "Задач пока нет")

    def test_list_shows_all_tasks(self):
        """В списке отображаются все созданные задачи"""
        Task.objects.create(title="First")
        Task.objects.create(title="Second")
        response = self.client.get(reverse("crud:task_list"))
        self.assertContains(response, "First")
        self.assertContains(response, "Second")
        self.assertEqual(len(response.context["tasks"]), 2)

    def test_list_contains_links_to_detail(self):
        """В списке есть ссылка на страницу детали задачи"""
        task = Task.objects.create(title="Linked")
        response = self.client.get(reverse("crud:task_list"))
        self.assertContains(response, reverse("crud:task_detail", args=[task.pk]))


class TaskDetailViewTests(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title="Detail", description="Some text")

    def test_detail_shows_content(self):
        """Страница детали показывает название и описание"""
        response = self.client.get(reverse("crud:task_detail", args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Detail")
        self.assertContains(response, "Some text")

    def test_detail_uses_correct_template(self):
        """Страница детали использует нужный шаблон"""
        response = self.client.get(reverse("crud:task_detail", args=[self.task.pk]))
        self.assertTemplateUsed(response, "crud/task_detail.html")

    def test_detail_returns_404_for_missing(self):
        """Несуществующая задача даёт 404"""
        response = self.client.get(reverse("crud:task_detail", args=[999]))
        self.assertEqual(response.status_code, 404)


class TaskCreateViewTests(TestCase):
    def test_create_form_opens(self):
        """GET открывает пустую форму создания"""
        response = self.client.get(reverse("crud:task_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "crud/task_form.html")

    def test_create_valid_data(self):
        """POST с корректными данными создаёт задачу и редиректит на список"""
        response = self.client.post(
            reverse("crud:task_create"),
            {"title": "New", "description": "Text"},
        )
        self.assertRedirects(response, reverse("crud:task_list"))
        self.assertTrue(Task.objects.filter(title="New", description="Text").exists())

    def test_create_with_done_checkbox(self):
        """Отмеченный чекбокс done сохраняется как True"""
        self.client.post(reverse("crud:task_create"), {"title": "Done task", "done": "on"})
        self.assertTrue(Task.objects.get(title="Done task").done)

    def test_create_without_done_checkbox(self):
        """Без чекбокса done задача сохраняется как невыполненная"""
        self.client.post(reverse("crud:task_create"), {"title": "Open task"})
        self.assertFalse(Task.objects.get(title="Open task").done)

    def test_create_empty_title_rejected(self):
        """Пустое название не проходит валидацию, задача не создаётся"""
        response = self.client.post(reverse("crud:task_create"), {"title": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.context["form"].errors)
        self.assertEqual(Task.objects.count(), 0)

    def test_create_too_long_title_rejected(self):
        """Название длиннее 200 символов не проходит валидацию"""
        response = self.client.post(reverse("crud:task_create"), {"title": "a" * 201})
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.context["form"].errors)
        self.assertEqual(Task.objects.count(), 0)


class TaskUpdateViewTests(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title="Old title", description="Old text")
        self.url = reverse("crud:task_update", args=[self.task.pk])

    def test_update_form_prefilled(self):
        """Форма редактирования открывается с текущими данными"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Old title")

    def test_update_changes_data(self):
        """POST меняет данные задачи и редиректит на список"""
        response = self.client.post(self.url, {"title": "New title", "description": "New text"})
        self.assertRedirects(response, reverse("crud:task_list"))
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "New title")
        self.assertEqual(self.task.description, "New text")

    def test_update_can_mark_done(self):
        """При редактировании задачу можно отметить выполненной"""
        self.client.post(self.url, {"title": "Old title", "done": "on"})
        self.task.refresh_from_db()
        self.assertTrue(self.task.done)

    def test_update_empty_title_rejected(self):
        """Пустое название при редактировании не сохраняется"""
        response = self.client.post(self.url, {"title": ""})
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Old title")

    def test_update_missing_returns_404(self):
        """Редактирование несуществующей задачи даёт 404"""
        response = self.client.get(reverse("crud:task_update", args=[999]))
        self.assertEqual(response.status_code, 404)


class TaskDeleteViewTests(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title="To delete")
        self.url = reverse("crud:task_delete", args=[self.task.pk])

    def test_delete_confirmation_page(self):
        """GET показывает страницу подтверждения и не удаляет задачу"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "crud/task_confirm_delete.html")
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_delete_removes_task(self):
        """POST удаляет задачу и редиректит на список"""
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("crud:task_list"))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_delete_missing_returns_404(self):
        """Удаление несуществующей задачи даёт 404"""
        response = self.client.post(reverse("crud:task_delete", args=[999]))
        self.assertEqual(response.status_code, 404)
