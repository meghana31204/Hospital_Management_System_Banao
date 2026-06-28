# Hospital Management System

## Project Description

This Hospital Management System is a web application developed using Django as part of the Python Developer Serverless Internship assignment.

The system provides separate dashboards for doctors and patients. Doctors can create their available appointment slots, while patients can view those slots and book appointments. Once an appointment is booked, Google Calendar events are automatically created for both the doctor and the patient, and a confirmation email is sent through a separate Python Serverless email service.

---

## Features

- User Registration
- User Login and Logout
- Role-Based Authentication (Doctor & Patient)
- Doctor Dashboard
- Create Availability Slots
- View Available Slots
- Patient Dashboard
- Book Doctor Appointments
- Google OAuth Integration
- Google Calendar Event Creation
- Serverless Email Notification Service
- Booking Confirmation Email

---

## Technologies Used

- Python
- Django
- SQLite3
- HTML
- CSS
- Bootstrap
- JavaScript
- Google OAuth 2.0
- Google Calendar API
- Serverless Framework
- serverless-offline
- Gmail SMTP

---

## Project Structure

```
Hospital_Management_System/
│
├── Hospital_Management_System/
├── accounts/
├── templates/
├── static/
├── email-service/
├── requirements.txt
├── README.md
├── .gitignore
└── manage.py
```

---

## How to Run the Project

### 1. Clone the Repository

```bash
git clone [<your-github-repository-link>](https://github.com/meghana31204/Hospital_Management_System_Banao.git)
```

### 2. Open the Project

```bash
cd Hospital_Management_System
```

### 3. Activate the Virtual Environment

```bash
venv\Scripts\activate
```

### 4. Install Required Packages

```bash
pip install -r requirements.txt
```

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Start the Django Server

```bash
python manage.py runserver
```

The application will run at:

```
http://127.0.0.1:8000/
```

---

## Running the Serverless Email Service

Open a new terminal.

Navigate to the email-service folder.

```bash
cd email-service
```

Run the Serverless service.

```bash
serverless.cmd offline
```

The email service will run locally on:

```
http://localhost:3000
```

---

## Application Workflow

1. A user registers as either a Doctor or a Patient.
2. The doctor logs in and creates appointment availability slots.
3. The patient logs in and views the available slots.
4. The patient books an appointment.
5. The application creates Google Calendar events for both the doctor and the patient.
6. Django sends the appointment details to the Serverless email service.
7. The Serverless function sends a booking confirmation email to the patient.

---

## Google OAuth

Google OAuth is used to authenticate users and obtain permission to access their Google Calendar.

After authorization, appointments are automatically added to both the doctor's and the patient's Google Calendar.

---

## Environment Variables

The project uses a `.env` file to securely store sensitive information such as:

- Gmail Email Address
- Gmail App Password
- Google Client ID
- Google Client Secret
- Google Redirect URI

The `.env` file is excluded from GitHub using `.gitignore`.

---

## Repository Contents

- Django Application
- Serverless Email Service
- README.md
- requirements.txt
- .gitignore
- AI Tool Usage Log

---

## Future Improvements

- Appointment Cancellation
- Appointment Rescheduling
- Admin Dashboard
- SMS Notifications
- Payment Integration

---

## Author

**Meghana Pavuluri**

Python Developer Serverless Internship Assignment
