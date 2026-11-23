from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class CaptchaAuthenticationForm(AuthenticationForm):
    """Форма входа с капчей: без правильного ответа на капчу войти нельзя."""
    captcha = CaptchaField(label="Проверка: решите пример")


class RegisterForm(UserCreationForm):
    """Регистрация: логин, email (обязательный и уникальный), пароль дважды."""
    email = forms.EmailField(required=True, label="Email")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email


class CabinetForm(forms.ModelForm):
    """Редактирование данных в личном кабинете. Логин изменить нельзя."""
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Этот email уже занят другим пользователем.")
        return email
