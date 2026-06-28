from django.contrib import admin

# Register your models here.
from .models import AvailabilitySlot, Booking

admin.site.register(AvailabilitySlot)
admin.site.register(Booking)