from django.urls import path

from . import views

app_name = "tours"

urlpatterns = [
    path("", views.tour_list, name="tour_list"),
    path("<int:pk>/", views.tour_detail, name="tour_detail"),
    path("<int:pk>/book/", views.book_tour, name="book_tour"),
    path("<int:pk>/comment/", views.add_comment, name="add_comment"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("profile/", views.profile_edit, name="profile_edit"),
]
