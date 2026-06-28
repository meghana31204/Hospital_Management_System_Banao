import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
from google_auth_oauthlib.flow import Flow
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth import authenticate, login, logout
from appointments.models import AvailabilitySlot, Booking
from django.db import transaction
from django.utils import timezone
from django.contrib import messages
from django.views.decorators.http import require_POST
from datetime import datetime
from appointments.calendar_service import create_calendar_event
import requests
# ----------------------------
# Signup
# ----------------------------
def home(request):
    return render(request, "home.html")
def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        email = request.POST["email"]
        password = request.POST["password"]
        role = request.POST["role"]
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

        # Duplicate email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("signup")

        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            role=role
        )
        try:
            requests.post(
                "http://localhost:3000/email",
                json={
                    "trigger": "SIGNUP_WELCOME",
                    "email": email,
                    "name": first_name
                },
                timeout=10
            )
        except requests.RequestException:
            # Continue even if email service is unavailable
            pass
        # Duplicate username
        

        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "signup.html")


# ----------------------------
# Login
# ----------------------------
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            if user.role == "doctor":
                return redirect("doctor_dashboard")

            elif user.role == "patient":
                return redirect("patient_dashboard")

            else:
                return redirect("admin:index")

        messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


# ----------------------------
# Logout
# ----------------------------
def logout_user(request):
    logout(request)
    return redirect("login")


# ----------------------------
# Doctor Dashboard
# ----------------------------
def doctor_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.role != "doctor":
        return redirect("login")

    if request.method == "POST":
        start_time = datetime.fromisoformat(request.POST["start_time"])
        end_time = datetime.fromisoformat(request.POST["end_time"])

        # Convert to timezone-aware datetime
        start_time = timezone.make_aware(start_time)
        end_time = timezone.make_aware(end_time)

        # Cannot create past slots
        if start_time <= timezone.now():
            messages.error(
                request,
                "You cannot create availability slots in the past."
            )
            return redirect("doctor_dashboard")

        # End time validation
        if start_time >= end_time:
            messages.error(
                request,
                "End time must be later than start time."
            )
            return redirect("doctor_dashboard")

        # Prevent overlapping slots
        overlapping_slot = AvailabilitySlot.objects.filter(
            doctor=request.user,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        if overlapping_slot:
            messages.error(
                request,
                "This availability slot overlaps with an existing slot."
            )
            return redirect("doctor_dashboard")

        AvailabilitySlot.objects.create(
            doctor=request.user,
            start_time=start_time,
            end_time=end_time
        )

        messages.success(
            request,
            "Availability slot created successfully."
        )

    slots = AvailabilitySlot.objects.filter(
        doctor=request.user
    ).order_by("start_time")

    bookings = Booking.objects.filter(
        slot__doctor=request.user
    ).order_by("-booked_at")

    return render(
        request,
        "doctor_dashboard.html",
        {
            "slots": slots,
            "bookings": bookings
        }
    )


# ----------------------------
# Patient Dashboard
# ----------------------------
def patient_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.role != "patient":
        return redirect("login")

    slots = AvailabilitySlot.objects.filter(
        is_booked=False,
        start_time__gt=timezone.now()
    ).order_by("start_time")

    return render(
        request,
        "patient_dashboard.html",
        {
            "slots": slots
        }
    )


# ----------------------------
# Book Appointment
# ----------------------------
@transaction.atomic
def book_slot(request, slot_id):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.role != "patient":
        return redirect("login")

    if request.method == "POST":
        slot = get_object_or_404(
            AvailabilitySlot.objects.select_for_update(),
            id=slot_id
        )

        if slot.is_booked:
            messages.error(
                request,
                "This slot has already been booked."
            )
            return redirect("patient_dashboard")

        Booking.objects.create(
            patient=request.user,
            slot=slot
        )

        slot.is_booked = True
        slot.save()

        try:
    # Create event in doctor's calendar
            create_calendar_event(
                slot.doctor,
                f"Appointment with {request.user.first_name} {request.user.last_name}",
                slot.start_time,
                slot.end_time,
                f"Patient: {request.user.first_name} {request.user.last_name}"
            )

            # Create event in patient's calendar
            create_calendar_event(
                request.user,
                f"Appointment with Dr. {slot.doctor.first_name} {slot.doctor.last_name}",
                slot.start_time,
                slot.end_time,
                f"Doctor: Dr. {slot.doctor.first_name} {slot.doctor.last_name}"
            )

        except Exception as e:
            print("Google Calendar Error:", e)

        try:
            response = requests.post(
                "http://localhost:3000/email",
                json={
                    "trigger": "BOOKING_CONFIRMATION",
                    "email": request.user.email,
                    "name": request.user.first_name
                },
                timeout=10
            )

            print("Status Code:", response.status_code)
            print("Response:", response.text)

        except Exception as e:
            print("Django Email Error:", e)

        messages.success(
            request,
            "Appointment booked successfully."
        )

    return redirect("patient_dashboard")

# ----------------------------
# Delete Slot
# ----------------------------
@require_POST
def delete_slot(request, slot_id):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.role != "doctor":
        return redirect("login")

    slot = get_object_or_404(
        AvailabilitySlot,
        id=slot_id,
        doctor=request.user
    )

    if not slot.is_booked:
        slot.delete()
        messages.success(
            request,
            "Slot deleted successfully."
        )
    else:
        messages.error(
            request,
            "Booked slots cannot be deleted."
        )

    return redirect("doctor_dashboard")
def google_login(request):
    flow = Flow.from_client_secrets_file(
        "credentials.json",
        scopes=[
            "https://www.googleapis.com/auth/calendar"
        ]
    )

    flow.redirect_uri = "http://127.0.0.1:8000/google/callback/"
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        prompt="consent",
        include_granted_scopes="true"
    )

    request.session["state"] = state
    request.session["code_verifier"] = flow.code_verifier

    return redirect(authorization_url)


def google_callback(request):

    state = request.session.get("state")

    flow = Flow.from_client_secrets_file(
        "credentials.json",
        scopes=[
            "https://www.googleapis.com/auth/calendar"
        ],
        state=state
    )

    flow.redirect_uri = "http://127.0.0.1:8000/google/callback/"

    flow.code_verifier = request.session.get("code_verifier")

    flow.fetch_token(
        authorization_response=request.build_absolute_uri()
    )

    credentials = flow.credentials

    request.user.google_credentials = credentials.to_json()

    request.user.save()

    messages.success(
        request,
        "Google Calendar connected successfully!"
    )

    if request.user.role == "doctor":
        return redirect("doctor_dashboard")

    return redirect("patient_dashboard")