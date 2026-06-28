from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("signup/", views.signup, name="signup"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),

    path("doctor-dashboard/", views.doctor_dashboard, name="doctor_dashboard"),
    path("patient-dashboard/", views.patient_dashboard, name="patient_dashboard"),

    path("book-slot/<int:slot_id>/", views.book_slot, name="book_slot"),

    path(
        "delete-slot/<int:slot_id>/",
        views.delete_slot,
        name="delete_slot",
    ),

    path("google/login/", views.google_login, name="google_login"),
    path("google/callback/", views.google_callback, name="google_callback"),
]