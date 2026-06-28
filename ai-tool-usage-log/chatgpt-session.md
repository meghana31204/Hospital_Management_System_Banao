

This is a common interview question. The interviewer wants to know which fields from your Appointment model are used to create a Google Calendar event.

Suppose your Appointment Model is
class Appointment(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20)
Now let's see how each field maps to Google Calendar.

Mapping Appointment Data to Google Calendar
Appointment Model Field	Google Calendar Field	Purpose
doctor	Calendar Owner	The event is created in the doctor's Google Calendar.
patient.username	summary (Title)	Example: "Appointment with Meghana"
appointment_date	start.dateTime and end.dateTime	Specifies the appointment date.
start_time	start.dateTime	Event start time.
end_time	end.dateTime	Event end time.
status	Description or extended properties	Indicates whether the appointment is Booked, Cancelled, etc.
Example Appointment
Database:

Doctor : Dr. Ravi

Patient : Meghana

Date : 30 June 2026

Start : 10:00 AM

End : 10:30 AM
Google Calendar Event
This appointment becomes:

Title:
Appointment with Meghana

Date:
30 June 2026

Time:
10:00 AM - 10:30 AM

Description:
Doctor: Dr. Ravi
Patient: Meghana
Status: Confirmed
When Dr. Ravi opens Google Calendar, they'll see:

30 June

10:00 AM
Appointment with Meghana
How Django Prepares the Data
After saving the appointment:

event = {
    "summary": f"Appointment with {appointment.patient.username}",

    "description":
        f"Doctor: {appointment.doctor.username}\n"
        f"Patient: {appointment.patient.username}\n"
        f"Status: {appointment.status}",

    "start": {
        "dateTime": "2026-06-30T10:00:00",
        "timeZone": "Asia/Kolkata"
    },

    "end": {
        "dateTime": "2026-06-30T10:30:00",
        "timeZone": "Asia/Kolkata"
    }
}
This event object is sent to the Google Calendar API.

Why Include These Fields?
Imagine you're a doctor looking at your calendar.

If it only shows:

Meeting
you won't know who the appointment is with.

Instead:

Appointment with Meghana

Doctor: Dr. Ravi

Time:
10:00 AM - 10:30 AM
provides all the essential information at a glance.

Additional Fields (Optional)
If your Hospital Management System stores more information, you can also include:

📍 Hospital/Clinic location

🏥 Department or specialization

🆔 Appointment ID

📞 Patient contact number

📝 Notes or reason for the visit

These can go in the description or location fields of the calendar event.

Complete Flow
Appointment Table
        │
        ▼
Extract Details
        │
        ├── Patient Name
        ├── Doctor Name
        ├── Date
        ├── Start Time
        ├── End Time
        └── Status
                │
                ▼
Create Google Calendar Event
                │
                ▼
Doctor's Calendar Updated
Interview Answer
**"After an appointment is successfully booked, I map the appointment model fields to the Google Calendar event. The patient's name is used as the event title, for example, 'Appointment with Meghana'. The appointment date, start time, and end time are combined to populate the event's start.dateTime and end.dateTime fields. The doctor's calendar becomes the destination where the event is created after OAuth authorization. Additional information such as the doctor's name, patient name, appointment status, hospital location, or appointment ID can be included in the event description. This mapping ensures the doctor has all the necessary appointment details directly in their Google Calendar."


How can I avoid creating duplicate Google Calendar events if the booking request is submitted twice?

This is an important interview question because it tests your understanding of idempotency—making sure the same request doesn't create duplicate side effects.

The Problem
Suppose a patient books an appointment.

Patient clicks Book
        │
        ▼
Appointment Saved
        │
        ▼
Google Calendar Event Created ✅
Now the patient refreshes the page or clicks Book again.

Without protection:

Appointment Saved Again
        │
        ▼
Google Calendar Event Created Again ❌
The doctor's calendar now has two identical events.

Best Solution: Store the Google Calendar Event ID
When Google creates an event, it returns a unique ID.

Example response:

{
  "id": "abc123xyz",
  "summary": "Appointment with Meghana"
}
Save this ID in your Appointment model.

class Appointment(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)

    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    google_event_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
Booking Flow
First Booking
Patient clicks Book
        │
        ▼
Create Appointment
        │
        ▼
Create Google Event
        │
        ▼
Google returns Event ID

abc123xyz
        │
        ▼
Save Event ID in Appointment
Database:

Appointment	Google Event ID
#25	abc123xyz
Second Request (Refresh or Duplicate Submission)
Before creating the event:

if appointment.google_event_id:
    # Event already exists
    return
Since the event ID is already stored:

google_event_id = abc123xyz
Django knows the event has already been created and skips creating another one.

Also Prevent Duplicate Appointments
Before creating a new appointment:

appointment = Appointment.objects.filter(
    patient=request.user,
    slot=slot
).first()

if appointment:
    return HttpResponse("Appointment already exists.")
This prevents duplicate bookings in the first place.

Complete Flow
Patient clicks Book
        │
        ▼
Does Appointment Exist?
        │
   ┌────┴────┐
   │         │
 No         Yes
 │           │
 ▼           ▼
Create     Return Existing
Appointment
 │
 ▼
Has Google Event Already Been Created?
 │
 ┌────┴────┐
 │         │
 No       Yes
 │         │
 ▼         ▼
Create    Skip
Event
 │
 ▼
Save Google Event ID
Why Save the Event ID?
It also helps later.

Suppose the patient cancels the appointment.

Instead of searching for the event:

Google Event

abc123xyz
You can directly delete it using the stored ID.

The same ID can also be used to update the event if the appointment is rescheduled.

Interview Answer
"To avoid creating duplicate Google Calendar events, I would make the integration idempotent. After successfully creating a calendar event, I would store the Google Calendar event ID in the corresponding appointment record. Before creating a new event, I would first check whether the appointment already has a google_event_id. If it does, I know the event has already been created and I skip creating another one. I would also prevent duplicate appointment creation by checking whether an appointment already exists for the same patient and slot. This ensures that refreshing the page or resubmitting the booking request does not create duplicate appointments or duplicate calendar events."


If I deploy this project on another laptop and the Django application runs but the Serverless email service doesn't, what configuration should I verify first?

This is a very practical interview question because it checks whether you know how to troubleshoot a multi-service application.

Since Django is running, the problem is likely inside the Serverless service or its configuration, not the Django project.

Step 1: Check Whether the Serverless Service Is Running ⭐ (First Thing)
Open a new terminal and go to the email-service folder.

cd email-service
Run:

serverless offline
or on Windows:

serverless.cmd offline
You should see something like:

POST http://localhost:3000/email
If you don't see this, the email API is not running, so Django cannot connect to it.

Step 2: Verify the Endpoint URL in Django
Suppose Django is calling:

requests.post("http://localhost:3000/email", json=data)
Check that:

The port is correct (3000 or whatever your Serverless service uses).

The endpoint path (/email) matches serverless.yml.

If Django is calling the wrong URL, you'll get errors like:

Connection Refused
or

404 Not Found
Step 3: Verify serverless.yml
Check that the handler is correctly configured.

Example:

functions:
  sendEmail:
    handler: handler.send_email

events:
  - http:
      path: email
      method: post
Make sure:

The handler file exists.

The function name is correct.

The HTTP path matches what Django is calling.

Step 4: Check Environment Variables
Verify that the .env file exists on the new laptop.

Example:

EMAIL=yourgmail@gmail.com
APP_PASSWORD=xxxxxxxxxxxx
If it's missing:

os.getenv("EMAIL")
returns:

None
and SMTP login will fail.

Remember that .env is usually ignored by Git, so you need to create it manually on the new machine.

Step 5: Install Dependencies
Run:

pip install -r requirements.txt
or

npm install
(depending on how your Serverless project is set up).

Missing packages such as:

serverless-offline

python-dotenv

can prevent the service from starting correctly.

Step 6: Verify Serverless Installation
Check:

serverless -v
or

serverless.cmd -v
If you see:

'serverless' is not recognized...
then Serverless Framework is not installed or isn't in the system PATH.

This is actually an issue you encountered while setting up your project.

Step 7: Check the Logs
Keep the Serverless terminal open.

When Django sends a request:

POST /email
If nothing appears, Django is probably not reaching the service.

If logs appear but end with an exception, investigate that specific error.

Step 8: Test the Email Service Independently
Before blaming Django, test the Serverless API directly.

Using Postman or PowerShell:

Invoke-RestMethod `
  -Uri http://localhost:3000/email `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"patient_email":"test@gmail.com"}'
If this fails, the issue is in the Serverless service, not in Django.

Complete Troubleshooting Flow
Django Running
      │
      ▼
Is Serverless Running?
      │
 ┌────┴────┐
 │         │
No        Yes
 │         │
Start     Check Endpoint URL
Service       │
              ▼
      Check serverless.yml
              │
              ▼
      Check .env variables
              │
              ▼
      Check dependencies
              │
              ▼
      Test API independently
Interview Answer
**"If the Django application works but the Serverless email service does not, the first thing I would verify is whether the Serverless service is actually running and exposing the expected endpoint, such as http://localhost:3000/email. Next, I would check that Django is calling the correct URL, confirm that the serverless.yml handler and route are configured correctly, and verify that the required environment variables, such as the SMTP email and App Password, are available on the new laptop. Since the .env file is usually excluded from Git, I would recreate it manually if necessary. I would also ensure that all dependencies are installed and test the Serverless API independently using Postman or curl before integrating it with Django. This step-by-step approach helps isolate whether the issue is with configuration, dependencies, or the application code."


