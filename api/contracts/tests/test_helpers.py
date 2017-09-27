# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core import mail
from mock import patch
from testfixtures import LogCapture


from contracts.management.helpers import send_template_mail


class MockMessage(object):
    def __init__(self, *args, **kwargs):
        super(MockMessage, *args, **kwargs)

    def send(self):
        raise Exception('Testing message')


class TestHelpers(TestCase):

    def test_send_email_building_failure(self):
        """
        Should log an error message when an exception happens while
        building the report email
        """
        with LogCapture() as output:
            with patch(
                'contracts.management.helpers.build_email_multi_alternative',
                    side_effect=Exception):
                    send_template_mail(
                        'Test', 'contracts_expiration_email.html',
                        ['user@fake.mail'])
        expected = (('contracts.management.helpers',
                     'ERROR',
                     'Failed building contracts expiration report email.'))
        output.check(expected)

    def test_send_email_sending_failure(self):
        """
        Should log an error message when an exception happens while
        sending the report email
        """
        with LogCapture() as output:
            with patch(
                'contracts.management.helpers.build_email_multi_alternative',
                    return_value=MockMessage()):
                    send_template_mail(
                        'Test', 'contracts_expiration_email.html',
                        ['user@fake.mail'])
        expected = (('contracts.management.helpers',
                     'ERROR',
                     'Failed sending contracts expiration report email.'))
        output.check(expected)

    def test_send_email_successfully(self):
        """Should successfully send e-mail with given template and data"""
        context = {
            'report': {
                'date': '2017-09-20 10:00:00',
                'contracts': [
                    {
                        'contract_id': '1',
                        'contract_url': ('http://localhost:8080/admin/'
                                         'contracts/contract/1/change/'),
                        'end_date': '2017-09-30',
                        'property': 'House at Baker Street, 101',
                        'tenant': 'John Doe',
                        'landlord': 'Vlad Dracul',
                        'rent': 1000.00
                    }
                ]
            }
        }
        send_template_mail('Testing email', 'contracts_expiration_email.html',
                           ['user.fake.mail'], context=context)
        content, mimetype = mail.outbox[0].alternatives[0]
        self.assertIn('Contracts reporting @ 2017-09-20 10:00:00', content)
        self.assertIn('Contract ID', content)
        self.assertIn('Ending Date', content)
        self.assertIn('Property', content)
        self.assertIn('Landlord', content)
        self.assertIn('Tenant', content)
        self.assertIn('Rent', content)
        self.assertIn(('<a href=\'http://localhost:8080/admin/contracts/'
                       'contract/1/change/\'> 1'), content)
        self.assertIn('House at Baker Street, 101', content)
        self.assertIn('John Doe', content)
