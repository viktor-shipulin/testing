from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import CabinetForm, CaptchaAuthenticationForm, RegisterForm


class CaptchaLoginView(LoginView):
    """Вход с капчей. Уже вошедшего пользователя отправляет в личный кабинет."""
    authentication_form = CaptchaAuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


def register(request):
    """Регистрация. После успешной регистрации пользователь сразу входит."""
    if request.user.is_authenticated:
        return redirect("cabinet")
    form = RegisterForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("cabinet")
    return render(request, "accounts/register.html", {"form": form})


@login_required
def cabinet(request):
    """Личный кабинет: данные текущего пользователя."""
    return render(request, "accounts/cabinet.html")


@login_required
def cabinet_edit(request):
    """Редактирование имени, фамилии и email."""
    form = CabinetForm(request.POST if request.method == "POST" else None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("cabinet")
    return render(request, "accounts/cabinet_edit.html", {"form": form})
