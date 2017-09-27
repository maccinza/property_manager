# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urlparse
import logging
from datetime import date, datetime, timedelta

from django.core.management.base import BaseCommand
from django.conf import settings
from validate_email import validate_email

from contracts.models import Contract
from contracts.management.helpers import send_template_mail

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = ('Checks for Contracts which are due to end within a week and '
            'sends an e-mail to given address')

    def add_arguments(self, parser):
        parser.add_argument(
            'email',
            help='e-mail to which the report should be sent')

    def handle(self, *args, **options):
        email = options['email']
        # if email is valid
        if validate_email(email):
            # filters contracts which ending date is within a week from now
            lower_limit = date.today()
            upper_limit = lower_limit + timedelta(days=7)
            contracts = Contract.objects.filter(
                end_date__range=[lower_limit, upper_limit]).select_related()
            # if it finds contracts
            if contracts:
                # collects contract info for reporting
                rhost = '{}:{}'.format(settings.HOST_NAME, settings.HOST_PORT)
                report = {
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'contracts': []
                }
                for contract in contracts:
                    data = {
                        'contract_id': contract.id,
                        'contract_url': urlparse.urljoin(
                            rhost, contract.get_admin_url()),
                        'end_date': contract.end_date.strftime('%Y-%m-%d'),
                        'property': contract.property.__unicode__(),
                        'tenant': contract.tenant.get_full_name(),
                        'landlord': contract.property.landlord.get_full_name(),
                        'rent': contract.rent
                    }
                    report['contracts'].append(data)
                # sends email with collected info
                send_template_mail(
                    'Contracts expiration report',
                    'contracts_expiration_email.html',
                    [email],
                    context={'report': report},
                    from_email='admbot@propertymgmt.com')
            else:
                msg = (u'There were no contracts with due date '
                       'to within one week')
                log.info(msg)
                print msg
        else:
            msg = u'Given e-mail "{}" is not valid.'.format(email)
            log.error(msg)
            print msg
