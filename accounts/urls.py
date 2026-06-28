from django.urls import path
from . import views
from django.views.generic import RedirectView
urlpatterns = [
    path("", RedirectView.as_view(pattern_name="login", permanent=False)),
    path('signup/',views.signup,name='signup'),
    path('login/', views.login_user, name='login'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('book-slot/<int:slot_id>/',views.book_slot,name='book_slot'),
    path('logout/', views.logout_user, name='logout'),
    path(
    'delete-slot/<int:slot_id>/',
    views.delete_slot,
    name='delete_slot'
),
]