from django.db import models

from accounts.models import User


class AvailabilitySlot(models.Model):
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'doctor'}
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    is_booked = models.BooleanField(default=False)
class Booking(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'patient'}
    )

    slot = models.OneToOneField(
        AvailabilitySlot,
        on_delete=models.CASCADE
    )

    booked_at = models.DateTimeField(auto_now_add=True)