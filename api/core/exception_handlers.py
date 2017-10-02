# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def parse_error_messages(message_container):
    """Best effort function that tries to parse error message into a plain string"""
    final_msg = ""
    if isinstance(message_container, dict):
        for key in message_container.keys():
            final_msg += "'{}': ".format(key)
            value = message_container[key]
            if isinstance(value, list):
                value = "; ".join(value)
                final_msg += value.replace('"', "'")
            else:
                value = str(value).replace('"', "'")
                final_msg += "{}. ".format(value)
    elif isinstance(message_container, list):
        final_msg += "; ".join(message_container)
    else:
        final_msg += str(message_container)
    return final_msg


def model_exception_handler(exc, context):
    """Catches django.core exceptions and standard python exceptions from the
    model level and converts them to a DRF Response object. All other
    exceptions are ignored and return as usual"""
    response = exception_handler(exc, context)
    if response:
        if (isinstance(response.data, list) or
           'detail' not in response.data.keys()):
            response.data = {'detail': parse_error_messages(response.data)}
    else:
        msg = exc.message
        if not msg and hasattr(exc, 'messages'):
            msg = '; '.join(exc.messages)
        response = Response(
            status=status.HTTP_400_BAD_REQUEST, data={'detail': msg}
        )
    return response
