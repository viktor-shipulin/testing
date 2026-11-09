from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm, CommentForm, ProfileForm
from .models import Booking, Category, Profile, Tour


def tour_list(request):
    """Список туров. Фильтр по категории: ?category=конный"""
    tours = Tour.objects.prefetch_related("categories")
    category = request.GET.get("category")
    if category:
        tours = tours.filter(categories__name=category)
    return render(request, "tours/tour_list.html", {
        "tours": tours,
        "categories": Category.objects.all(),
        "selected": category,
    })


def tour_detail(request, pk):
    """Страница тура: описание, категории, комментарии."""
    tour = get_object_or_404(Tour, pk=pk)
    return render(request, "tours/tour_detail.html", {
        "tour": tour,
        "comments": tour.comments.select_related("user"),
    })


@login_required
def book_tour(request, pk):
    """Покупка тура на выбранные день и время."""
    tour = get_object_or_404(Tour, pk=pk)
    form = BookingForm(request.POST or None, user=request.user, tour=tour)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("tours:my_bookings")
    return render(request, "tours/form.html", {"form": form, "title": f"Купить тур: {tour.title}"})


@login_required
def add_comment(request, pk):
    """Комментарий к туру. Разрешён только если у пользователя есть бронь."""
    tour = get_object_or_404(Tour, pk=pk)
    form = CommentForm(request.POST or None, user=request.user, tour=tour)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("tours:tour_detail", pk=tour.pk)
    return render(request, "tours/form.html", {"form": form, "title": f"Комментарий к туру: {tour.title}"})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related("tour")
    return render(request, "tours/my_bookings.html", {"bookings": bookings})


@login_required
def profile_edit(request):
    """Редактирование профиля (связь один к одному с User)."""
    profile, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("tours:my_bookings")
    return render(request, "tours/form.html", {"form": form, "title": "Мой профиль"})
