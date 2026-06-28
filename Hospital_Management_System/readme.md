# Hospital Management System

A Django-based Hospital Management System that allows doctors to manage their availability and enables patients to book appointments. The system includes role-based authentication, appointment booking with race condition handling, Google Calendar integration for both doctors and patients, and a separate Serverless email service for sending welcome and booking confirmation emails. The entire application is designed to run locally.
---
## Setup and Run

### Prerequisites

- Python 3.10 or above
- Node.js and npm
- Serverless Framework
- Google Cloud OAuth Credentials

### Clone the Repository

```bash
git clone https://github.com/meghana31204/Hospital_Management_System_Banao.git
cd Hospital_Management_System_Banao
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Configure Google Calendar

1. Create OAuth 2.0 credentials in Google Cloud Console.
2. Download the OAuth Client credentials.
3. Rename the downloaded file to:

```
credentials.json
```

4. Place the file in the project root directory.

### Run the Django Application

---> python manage.py runserver

The application will be available at:

```
http://127.0.0.1:8000/
```

### Run the Serverless Email Service

Open another terminal.

Navigate to the email-service folder. ----> cd email-service

Run:
serverless.cmd offline


The email service will be available at:

```
http://localhost:3000/
```

After both services are running, the application is ready for use.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------

## System Architecture

The project consists of two independent components that communicate through HTTP requests.

### Django Backend

The Django application is responsible for:

- User authentication using Django Authentication.
- Role-based access control for doctors and patients.
- Doctor dashboard for creating and managing availability slots.
- Patient dashboard for viewing and booking available appointments.
- Preventing duplicate bookings using database transactions.
- Google Calendar OAuth2 integration.
- Creating calendar events for both doctors and patients after successful appointment booking.

### Serverless Email Service

A separate Python serverless application built using the Serverless Framework handles email notifications.

The service supports two triggers:

- **SIGNUP_WELCOME** – sends a welcome email after user registration.
- **BOOKING_CONFIRMATION** – sends a confirmation email after an appointment is booked.

The Django application invokes the serverless function through its local HTTP endpoint running with `serverless-offline`.

### Data Model

The application uses three primary models:

**User**
- Extends Django's AbstractUser.
- Stores user role (Doctor or Patient).
- Stores Google Calendar OAuth credentials.

**AvailabilitySlot**
- Stores doctor's available appointment slots.
- Tracks whether a slot has already been booked.

**Booking**
- Stores appointment details between a doctor and a patient.
- Links a patient to a booked availability slot.

### Role-Based Access

Doctors can:

- Create availability slots.
- View their own bookings.
- Delete only their own available slots.

Patients can:

- View only available future slots.
- Book an appointment.
- Cannot access doctor-specific functionality.

### Google Calendar Integration

Doctors and patients authenticate with Google using OAuth2.

Once an appointment is successfully booked:

- An appointment event is created in the doctor's Google Calendar.
- An appointment event is created in the patient's Google Calendar.

The event contains:

- Appointment title
- Start time
- End time
- Appointment description

---

## The Design Decision

### Problem

The application must prevent multiple patients from booking the same appointment slot simultaneously.

### Option 1

Before creating a booking, simply check whether the selected slot has already been booked.

Although this approach is straightforward, it does not protect against concurrent requests. If two patients attempt to book the same slot at nearly the same time, both requests could pass the availability check before either booking is saved, resulting in duplicate bookings.

### Option 2 (Chosen)

Use Django's `transaction.atomic()` together with `select_for_update()`.

This approach locks the selected availability slot while the booking transaction is being processed. Only one request can modify the slot at a time, ensuring that once a booking is completed, any subsequent request recognizes that the slot has already been booked.

### Why I Chose This Approach

I selected this approach because it provides reliable protection against race conditions while maintaining data consistency. Although it introduces slightly more complexity, it guarantees that each appointment slot can only be booked once, which is essential for a hospital appointment system.

---
## Limitations

This project is intended for local demonstration and evaluation.

Current limitations include:

- SQLite is used for local development instead of PostgreSQL.
- Google OAuth credentials are stored locally.
- The Serverless email service is configured for local execution using `serverless-offline`.
- Appointment cancellation and rescheduling are not implemented.
- There is no administrator dashboard.
- The project has not been deployed to a production environment.
- Additional production-level validation, monitoring, and security improvements would be required before real-world deployment.
