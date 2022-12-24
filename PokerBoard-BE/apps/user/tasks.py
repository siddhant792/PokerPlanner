import logging
import smtplib

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from poker.celery import app

from apps.user import constants as user_constants

logger = logging.getLogger(__name__)


@app.task
def send_email_task(first_name, pk, token, email):
    """
    Celery task for sending email
    """
    message = render_to_string('user/email_template.html', {
        'username': first_name,
        'domain': settings.BASE_URL_FE,
        'uid': pk,
        'token': token
    })
    subject = render_to_string("user/email_subject_template.html", {
        "subject": user_constants.EMAIL_REGISTER_SUBJECT
    })
    try:
        send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[email], fail_silently=False)
    except smtplib.SMTPException as e:
        logger.error(e)
