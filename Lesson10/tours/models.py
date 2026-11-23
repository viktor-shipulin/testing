from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Category(models.Model):
    """Категория тура: конный, пеший, мото и т.д."""
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Tour(models.Model):
    """Тур. Связь многие ко многим с Category."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    categories = models.ManyToManyField(Category, related_name="tours")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Profile(models.Model):
    """Профиль туриста. Связь один к одному с User."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tour_profile",
    )
    phone = models.CharField(max_length=30, blank=True)
    riding_experience = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"Профиль {self.user}"


class Booking(models.Model):
    """Покупка тура. Один человек: один тур на конкретные день и время."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="bookings")
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "time"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date", "time"],
                name="unique_booking_per_user_date_time",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.tour} ({self.date} {self.time})"


class Comment(models.Model):
    """Комментарий к туру. Можно оставить несколько, но только к туру, который куплен."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tour_comments",
    )
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if self.user_id and self.tour_id:
            if not Booking.objects.filter(user_id=self.user_id, tour_id=self.tour_id).exists():
                raise ValidationError("Комментировать можно только тур, на который есть бронь.")

    def __str__(self):
        return f"{self.user} о {self.tour}"
