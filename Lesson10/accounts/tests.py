from captcha.models import CaptchaStore
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()

PASSWORD = "Str0ngPass!2026"


def captcha_data(correct=True):
    """Создаёт капчу в базе и возвращает поля формы с верным или неверным ответом."""
    key = CaptchaStore.generate_key()
    answer = CaptchaStore.objects.get(hashkey=key).response
    return {"captcha_0": key, "captcha_1": answer if correct else "wrong-answer"}


def login_data(username="anna", password=PASSWORD, correct_captcha=True):
    data = {"username": username, "password": password}
    data.update(captcha_data(correct_captcha))
    return data


class RegistrationTests(TestCase):
    """Регистрация нового пользователя"""

    def setUp(self):
        self.url = reverse("register")
        self.data = {
            "username": "anna",
            "email": "anna@example.com",
            "password1": PASSWORD,
            "password2": PASSWORD,
        }

    def test_register_page_opens(self):
        """Страница регистрации открывается"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_valid_registration_creates_user_and_logs_in(self):
        """Корректная регистрация создаёт пользователя, входит в аккаунт и ведёт в кабинет"""
        response = self.client.post(self.url, self.data)
        self.assertRedirects(response, reverse("cabinet"))
        self.assertTrue(User.objects.filter(username="anna", email="anna@example.com").exists())
        self.assertIn("_auth_user_id", self.client.session)

    def test_password_is_hashed(self):
        """Пароль хранится в виде хэша, а не открытым текстом"""
        self.client.post(self.url, self.data)
        user = User.objects.get(username="anna")
        self.assertNotEqual(user.password, PASSWORD)
        self.assertTrue(user.check_password(PASSWORD))

    def test_password_mismatch_rejected(self):
        """Разные пароли не проходят проверку"""
        self.data["password2"] = "Other0Pass!2026"
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("password2", response.context["form"].errors)
        self.assertEqual(User.objects.count(), 0)

    def test_weak_password_rejected(self):
        """Слишком простой пароль отклоняется"""
        self.data["password1"] = self.data["password2"] = "12345678"
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("password2", response.context["form"].errors)
        self.assertEqual(User.objects.count(), 0)

    def test_duplicate_username_rejected(self):
        """Занятый логин отклоняется"""
        User.objects.create_user("anna", "old@example.com", PASSWORD)
        response = self.client.post(self.url, self.data)
        self.assertIn("username", response.context["form"].errors)
        self.assertEqual(User.objects.count(), 1)

    def test_duplicate_email_rejected_case_insensitive(self):
        """Занятый email отклоняется независимо от регистра"""
        User.objects.create_user("boris", "ANNA@example.com", PASSWORD)
        response = self.client.post(self.url, self.data)
        self.assertIn("email", response.context["form"].errors)
        self.assertEqual(User.objects.count(), 1)

    def test_empty_email_rejected(self):
        """Пустой email отклоняется"""
        self.data["email"] = ""
        response = self.client.post(self.url, self.data)
        self.assertIn("email", response.context["form"].errors)
        self.assertEqual(User.objects.count(), 0)

    def test_invalid_email_rejected(self):
        """Email неверного формата отклоняется"""
        self.data["email"] = "not-an-email"
        response = self.client.post(self.url, self.data)
        self.assertIn("email", response.context["form"].errors)
        self.assertEqual(User.objects.count(), 0)

    def test_empty_form_rejected(self):
        """Пустая форма показывает ошибки обязательных полей"""
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(User.objects.count(), 0)

    def test_authenticated_user_redirected(self):
        """Вошедший пользователь со страницы регистрации попадает в кабинет"""
        User.objects.create_user("anna", "anna@example.com", PASSWORD)
        self.client.login(username="anna", password=PASSWORD)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("cabinet"))


class LoginCaptchaTests(TestCase):
    """Вход в аккаунт с учётом капчи"""

    def setUp(self):
        self.user = User.objects.create_user("anna", "anna@example.com", PASSWORD)
        self.url = reverse("login")

    def test_login_page_has_captcha(self):
        """Страница входа открывается и содержит поле капчи"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("captcha", response.context["form"].fields)

    def test_login_success_with_correct_captcha(self):
        """Верные данные и верная капча: вход выполнен, редирект в кабинет"""
        response = self.client.post(self.url, login_data())
        self.assertRedirects(response, reverse("cabinet"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_wrong_captcha_blocks_login(self):
        """Верный пароль, но неверная капча: войти нельзя"""
        response = self.client.post(self.url, login_data(correct_captcha=False))
        self.assertEqual(response.status_code, 200)
        self.assertIn("captcha", response.context["form"].errors)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_missing_captcha_blocks_login(self):
        """Верный пароль, но капча не заполнена: войти нельзя"""
        response = self.client.post(self.url, {"username": "anna", "password": PASSWORD})
        self.assertEqual(response.status_code, 200)
        self.assertIn("captcha", response.context["form"].errors)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_unknown_captcha_key_blocks_login(self):
        """Несуществующий ключ капчи не принимается"""
        data = {"username": "anna", "password": PASSWORD, "captcha_0": "unknown", "captcha_1": "1"}
        response = self.client.post(self.url, data)
        self.assertIn("captcha", response.context["form"].errors)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_wrong_password_with_correct_captcha(self):
        """Верная капча, но неверный пароль: войти нельзя"""
        response = self.client.post(self.url, login_data(password="WrongPass!2026"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].non_field_errors())
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_unknown_user_with_correct_captcha(self):
        """Несуществующий пользователь не может войти даже с верной капчей"""
        response = self.client.post(self.url, login_data(username="ghost"))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_captcha_is_single_use(self):
        """Одну и ту же капчу нельзя использовать дважды"""
        data = login_data()
        self.client.post(self.url, data)
        self.client.post(reverse("logout"))
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("captcha", response.context["form"].errors)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_respects_next_parameter(self):
        """После входа пользователь попадает на страницу из параметра next"""
        response = self.client.post(self.url + "?next=/tours/my-bookings/", login_data())
        self.assertRedirects(response, "/tours/my-bookings/", fetch_redirect_response=False)

    def test_authenticated_user_redirected_from_login(self):
        """Вошедший пользователь со страницы входа попадает в кабинет"""
        self.client.login(username="anna", password=PASSWORD)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("cabinet"))

    def test_logout_ends_session(self):
        """POST на выход завершает сессию"""
        self.client.login(username="anna", password=PASSWORD)
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_get_not_allowed(self):
        """GET-запрос на выход не разрешён"""
        self.client.login(username="anna", password=PASSWORD)
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 405)


class CabinetTests(TestCase):
    """Личный кабинет"""

    def setUp(self):
        self.user = User.objects.create_user(
            "anna", "anna@example.com", PASSWORD, first_name="Анна", last_name="Иванова"
        )
        self.other = User.objects.create_user("boris", "boris@example.com", PASSWORD)
        self.edit_url = reverse("cabinet_edit")

    def test_cabinet_requires_login(self):
        """Анонимного пользователя перенаправляют на страницу входа"""
        response = self.client.get(reverse("cabinet"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_edit_requires_login(self):
        """Страница редактирования недоступна без входа"""
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_cabinet_shows_own_data(self):
        """Кабинет показывает данные текущего пользователя"""
        self.client.login(username="anna", password=PASSWORD)
        response = self.client.get(reverse("cabinet"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "anna@example.com")
        self.assertContains(response, "Анна")

    def test_cabinet_hides_other_users_data(self):
        """Кабинет не показывает данные других пользователей"""
        self.client.login(username="anna", password=PASSWORD)
        response = self.client.get(reverse("cabinet"))
        self.assertNotContains(response, "boris@example.com")

    def test_edit_form_prefilled(self):
        """Форма редактирования открывается с текущими данными"""
        self.client.login(username="anna", password=PASSWORD)
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "anna@example.com")

    def test_edit_updates_data(self):
        """POST обновляет имя, фамилию и email и ведёт в кабинет"""
        self.client.login(username="anna", password=PASSWORD)
        response = self.client.post(self.edit_url, {
            "first_name": "Анастасия",
            "last_name": "Петрова",
            "email": "new@example.com",
        })
        self.assertRedirects(response, reverse("cabinet"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Анастасия")
        self.assertEqual(self.user.last_name, "Петрова")
        self.assertEqual(self.user.email, "new@example.com")

    def test_edit_invalid_email_rejected(self):
        """Неверный email не сохраняется"""
        self.client.login(username="anna", password=PASSWORD)
        response = self.client.post(self.edit_url, {"first_name": "А", "last_name": "И", "email": "bad"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("email", response.context["form"].errors)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "anna@example.com")

    def test_edit_duplicate_email_rejected(self):
        """Email другого пользователя занять нельзя"""
        self.client.login(username="anna", password=PASSWORD)
        response = self.client.post(self.edit_url, {
            "first_name": "А", "last_name": "И", "email": "boris@example.com",
        })
        self.assertIn("email", response.context["form"].errors)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "anna@example.com")

    def test_edit_keeps_own_email(self):
        """Сохранение со своим же email не считается дубликатом"""
        self.client.login(username="anna", password=PASSWORD)
        response = self.client.post(self.edit_url, {
            "first_name": "Анна", "last_name": "Иванова", "email": "anna@example.com",
        })
        self.assertRedirects(response, reverse("cabinet"))

    def test_username_cannot_be_changed(self):
        """Логин нельзя изменить через форму кабинета"""
        self.client.login(username="anna", password=PASSWORD)
        self.client.post(self.edit_url, {
            "first_name": "Анна", "last_name": "Иванова",
            "email": "anna@example.com", "username": "hacker",
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "anna")
