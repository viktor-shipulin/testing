from django import forms

from .models import Booking, Comment, Profile


class BookingForm(forms.ModelForm):
    """Покупка тура на дату и время. Пользователь и тур подставляются из view."""

    class Meta:
        model = Booking
        fields = ["date", "time"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, user=None, tour=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.tour = tour

    def clean(self):
        cleaned = super().clean()
        date = cleaned.get("date")
        time = cleaned.get("time")
        if self.user and date and time:
            if Booking.objects.filter(user=self.user, date=date, time=time).exists():
                raise forms.ValidationError("У вас уже куплен тур на это время.")
        return cleaned

    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.user = self.user
        booking.tour = self.tour
        if commit:
            booking.save()
        return booking


class CommentForm(forms.ModelForm):
    """Комментарий к туру. Модель сама проверит, что у пользователя есть бронь."""

    class Meta:
        model = Comment
        fields = ["text"]

    def __init__(self, *args, user=None, tour=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.user = user
        self.instance.tour = tour


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone", "riding_experience"]
