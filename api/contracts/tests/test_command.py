# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core import mail
from django.core.management import call_command
from testfixtures import LogCapture
from freezegun import freeze_time

from contracts.tests.factories import ContractFactory


class TestContractsReportCommand(TestCase):

    def setUp(self):
        self.contract_one = ContractFactory()
        self.contract_two = ContractFactory()

    def test_call_command_invalid_email(self):
        """
        Should log message and inform user that provided email is invalid
        """
        with LogCapture() as output:
            call_command('check_contracts', 'invalid-email')
        expected = (('contracts.management.commands.check_contracts',
                     'ERROR',
                     u'Given e-mail "invalid-email" is not valid.'))
        output.check(expected)

    @freeze_time('2017-09-24')
    def test_call_command_no_contracts(self):
        """
        Should log message and inform user that there were no contracts
        matching the search requirements
        """
        with LogCapture() as output:
            call_command('check_contracts', 'report@fake.mail')
        expected = (('contracts.management.commands.check_contracts',
                     'INFO',
                     (u'There were no contracts with due date '
                      'to within one week')))
        output.check(expected)

    @freeze_time('2018-09-20')
    def test_call_command_send_report(self):
        """
        Should send email report containing the data of contracts matching
        search requirements
        """
        call_command('check_contracts', 'report@fake.mail')
        content, mimetype = mail.outbox[0].alternatives[0]
        self.assertIn('<a href=\'http://localhost:8000/admin/contracts/'
                      'contract/{}/change/\'> '
                      '{} </a>'.format(self.contract_one.id,
                                       self.contract_one.id), content)
        self.assertIn('<td> {} </td>'.format(
            self.contract_one.end_date.strftime(
            '%Y-%m-%d')), content)
        self.assertIn('<td> {} </td>'.format(
            self.contract_one.property.__unicode__()), content)
        self.assertIn('<td> {} </td>'.format(
            self.contract_one.property.landlord.get_full_name()), content)
        self.assertIn('<td> {} </td>'.format(
            self.contract_one.tenant.get_full_name()), content)
        self.assertIn('<td> {}'.format(self.contract_one.rent), content)
        self.assertIn('<td> <a href=\'http://localhost:8000/admin/contracts'
                      '/contract/{}/change/\'> '
                      '{} </a></td>'.format(self.contract_two.id,
                                            self.contract_two.id), content)
        self.assertIn('<td> {} </td>'.format(
            self.contract_two.end_date.strftime(
            '%Y-%m-%d')), content)
        self.assertIn('<td> {} </td>'.format(
            self.contract_two.property.__unicode__()), content)
        self.assertIn('<td> {} </td>'.format(
            self.contract_two.property.landlord.get_full_name()), content)
        self.assertIn('<td> {} </td>'.format(
            self.contract_two.tenant.get_full_name()), content)
        self.assertIn('<td> {}'.format(self.contract_two.rent), content)
