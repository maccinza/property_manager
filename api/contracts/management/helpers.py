# -*- encoding: UTF-8 -*-
import logging

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import get_connection, EmailMultiAlternatives

log = logging.getLogger(__name__)


def build_email_multi_alternative(subject, template, recipient_list,
                                  context=None, from_email=None,
                                  connection=None, auth_user=None,
                                  auth_password=None, fail_silently=False,
                                  **kwargs):
    context = context or {}

    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )

    html_message = render_to_string(template, context=context)
    text_message = strip_tags(html_message)

    mail = EmailMultiAlternatives(
        subject, text_message, from_email,
        recipient_list, connection=connection)
    mail.attach_alternative(html_message, 'text/html')
    return mail


def send_template_mail(subject, template, recipient_list, context=None,
                       from_email=None, **kwargs):
    """Extends django.core.mail.send_mail to accept HTML templates"""
    try:
        message = build_email_multi_alternative(
            subject, template, recipient_list, context, from_email, **kwargs)
    except Exception:
        log.error('Failed building contracts expiration report email.')
        return
    try:
        return message.send()
    except Exception:
        log.error('Failed sending contracts expiration report email.')
