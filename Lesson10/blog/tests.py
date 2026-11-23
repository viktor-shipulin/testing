from django.test import TestCase
from django.urls import reverse

from .models import Blog


class BlogListTests(TestCase):
    def setUp(self):
        self.blog = Blog.objects.create(title="Первый пост", content="Текст поста")

    def test_list_status_200(self):
        response = self.client.get(reverse("blog_list"))
        self.assertEqual(response.status_code, 200)

    def test_list_contains_blog_title(self):
        response = self.client.get(reverse("blog_list"))
        self.assertContains(response, "Первый пост")

    def test_list_empty_has_no_blogs(self):
        Blog.objects.all().delete()
        response = self.client.get(reverse("blog_list"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Первый пост")

    def test_list_has_link_to_detail(self):
        response = self.client.get(reverse("blog_list"))
        detail_url = reverse("blog_detail", args=[self.blog.pk])
        self.assertContains(response, detail_url)

    def test_list_link_leads_to_detail(self):
        detail_url = reverse("blog_detail", args=[self.blog.pk])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)


class BlogDetailTests(TestCase):
    def setUp(self):
        self.blog = Blog.objects.create(title="Пост", content="Содержимое")
        self.url = reverse("blog_detail", args=[self.blog.pk])

    def test_detail_status_200(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_detail_shows_content(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Содержимое")

    def test_detail_nonexistent_id_returns_404(self):
        response = self.client.get(reverse("blog_detail", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_detail_has_correct_object_in_context(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context["object"].pk, self.blog.pk)


class BlogLikesTests(TestCase):
    def test_new_blog_has_zero_likes(self):
        blog = Blog.objects.create(title="Новый", content="Текст")
        self.assertEqual(blog.likes, 0)

    def test_detail_view_increments_likes(self):
        blog = Blog.objects.create(title="Новый", content="Текст")
        self.client.get(reverse("blog_detail", args=[blog.pk]))
        blog.refresh_from_db()
        self.assertEqual(blog.likes, 1)
