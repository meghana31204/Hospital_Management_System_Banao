import json
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


def send_email(event, context):
    try:
        body = event.get("body", {})

        if isinstance(body, str):
            body = json.loads(body)

        trigger = body.get("trigger")
        recipient = body.get("email")
        name = body.get("name", "User")

        sender_email = os.getenv("EMAIL_ADDRESS")
        sender_password = os.getenv("EMAIL_PASSWORD")

        if trigger == "SIGNUP_WELCOME":
            subject = "Welcome to Hospital Management System"
            message = f"""
Hello {name},

Welcome to the Hospital Management System!

Your account has been created successfully.

Thank you,
Hospital Management Team
"""

        elif trigger == "BOOKING_CONFIRMATION":
            subject = "Appointment Booking Confirmation"
            message = f"""
Hello {name},

Your appointment has been booked successfully.

Thank you,
Hospital Management Team
"""

        else:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Invalid trigger"
                })
            }

        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient

        with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"{trigger} email sent successfully."
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }