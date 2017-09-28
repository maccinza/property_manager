# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core import mail
from django.core.management import call_command
from testfixtures import LogCapture
from freezegun import freeze_time

from contracts.models import Contract
from accounts.models import Landlord, Tenant
from properties.models import Property


class TestContractsReportCommand(TestCase):

    def setUp(self):
        self.landlord_one = Landlord.objects.create(
            email='landone@fake.mail',
            first_name='John',
            last_name='Snow',
            password='secret123')

        self.landlord_two = Landlord.objects.create(
            email='landtwo@fake.mail',
            first_name='Daenerys',
            last_name='Targaryen',
            password='secret123')

        self.property_one = Property.objects.create(
            street='Baker Street',
            number='100',
            zip_code='NW16XE',
            city='London',
            description='Awesome description.',
            category='house',
            beds='2',
            landlord=self.landlord_one)

        self.property_two = Property.objects.create(
            street='Elm Street',
            number='200',
            zip_code='NU16XO',
            city='Nowhere Land',
            description='Fantastic description.',
            category='apartment',
            beds='1',
            landlord=self.landlord_two)

        self.tenant_one = Tenant.objects.create(
            email='tenantone@fake.mail',
            first_name='Agatha',
            last_name='Christie',
            password='secret123')

        self.tenant_two = Tenant.objects.create(
            email='tenanttwo@fake.mail',
            first_name='John',
            last_name='Tolkien',
            password='secret123')

        self.contract_one = Contract.objects.create(
            start_date='2016-09-20',
            end_date='2017-09-20',
            rent=1100.00,
            property=self.property_one,
            tenant=self.tenant_one)

        self.contract_two = Contract.objects.create(
            start_date='2016-09-23',
            end_date='2017-09-23',
            rent=950.00,
            property=self.property_two,
            tenant=self.tenant_two)

        self.contract_three = Contract.objects.create(
            start_date='2017-10-23',
            end_date='2018-10-23',
            rent=1000.00,
            property=self.property_two,
            tenant=self.tenant_one)

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

    @freeze_time('2017-09-19')
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
        self.assertIn('<td> 2017-09-20 </td>', content)
        self.assertIn('<td> House at Baker Street, 100 - London </td>',
                      content)
        self.assertIn('<td> John Snow </td>', content)
        self.assertIn('<td> Agatha Christie </td>', content)
        self.assertIn('<td> 1100.00', content)
        self.assertIn('<td> <a href=\'http://localhost:8000/admin/contracts'
                      '/contract/{}/change/\'> '
                      '{} </a></td>'.format(self.contract_two.id,
                                            self.contract_two.id), content)
        self.assertIn('<td> 2017-09-23 </td>', content)
        self.assertIn('<td> Apartment at Elm Street, 200 - '
                      'Nowhere Land </td>', content)
        self.assertIn('<td> Daenerys Targaryen </td>', content)
        self.assertIn('<td> John Tolkien </td>', content)
        self.assertIn('<td> 950.00', content)
        self.assertNotIn('<td> <a href=\'http://localhost:8000/admin/contracts'
                         '/contract/{}/change/\'> '
                         '{} </a></td>'.format(self.contract_three.id,
                                               self.contract_three.id),
                         content)
