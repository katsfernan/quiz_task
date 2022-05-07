from celery import shared_task
import smtplib
from quizzes_task.settings import (
    EMAIL_HOST_USER,
    EMAIL_HOST,
    EMAIL_PORT,
    EMAIL_HOST_PASSWORD
    )
import smtplib, ssl
from email.message import EmailMessage

@shared_task
def send_email_task(subject, message, receivers):
    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_HOST_USER
    msg["To"] = receivers
    context=ssl.create_default_context()

    with smtplib.SMTP(host= EMAIL_HOST, port = EMAIL_PORT) as smtp:
        smtp.starttls(context=context)
        smtp.login(msg["From"],EMAIL_HOST_PASSWORD )
        smtp.send_message(msg)