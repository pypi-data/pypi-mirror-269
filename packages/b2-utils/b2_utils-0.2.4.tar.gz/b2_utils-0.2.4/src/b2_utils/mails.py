from django.conf import settings as _settings
from django.core.mail import send_mail as _send_mail

__all__ = [
    "send_mail_template",
]


def send_mail_template(subject, html_message, plain_message, email):
    _send_mail(
        subject,
        plain_message,
        _settings.DEFAULT_FROM_EMAIL,
        [
            email,
        ],
        html_message=html_message,
    )
