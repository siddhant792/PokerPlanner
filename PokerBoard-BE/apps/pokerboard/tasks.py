from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from poker.celery import app


@app.task
def send_email_task(invite_id, email, pokerboard, role):
    """
    Celery task for sending invitation email
    """
    template = render_to_string("pokerboard/email_template.html", {
        "invite_id": invite_id,
        "pokerboard": pokerboard,
        "role": role,
        "domain": settings.BASE_URL_FE,
    })
    subject = render_to_string("pokerboard/email_subject_template.html", {"pokerboard": pokerboard})
    send_mail(subject=subject, message="", html_message=template, from_email=settings.EMAIL_HOST_USER, recipient_list=[email])
