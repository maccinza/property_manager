# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from accounts.models import Tenant
from properties.models import Property


class Contract(models.Model):
    """Contract representation"""

    created = models.DateTimeField(
        auto_now_add=True, help_text=u'contract creation date and time')
    start_date = models.DateField(help_text=u'starting date for the contract')
    end_date = models.DateField(help_text=u'ending date for the contract')
    property = models.ForeignKey(
        Property, help_text=u'property associated with the contract')
    tenant = models.ForeignKey(
        Tenant, help_text=u'tenant associated with the contract')
    rent = models.DecimalField(
        max_digits=10, decimal_places=2,
        help_text=u'monthly value in pounds that should be payed by tenant')

    def __unicode__(self):
        rep = 'Tenant {} - Property #{}, from {} to {}'.format(
            self.tenant.get_full_name(), self.property.id,
            self.start_date.strftime('%Y-%m-%d'),
            self.end_date.strftime('%Y-%m-%d'))
        return rep

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Contract, self).save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        # if all required fields were provided
        if self.tenant and self.property and self.start_date and self.end_date:
            # filters existing contracts for checking if there is a contract
            # which includes the property or tenant with overlapping dates
            contracts = Contract.objects.filter(
                models.Q(tenant=self.tenant) |
                models.Q(property=self.property),
                models.Q(start_date__range=[self.start_date, self.end_date]) |
                models.Q(end_date__range=[self.start_date, self.end_date]))
            if self.id:
                # excludes itself from the filter in a case of update
                contracts = contracts.exclude(id=self.id)
            if contracts:
                raise ValidationError(
                    u'There is already another contract for this property or '
                    'for this tenant and the given dates.')
            # end date should be greater than start date
            if not self.end_date > self.start_date:
                raise ValidationError(
                    u'Invalid dates for contract. Ending date come after '
                    'starting date.')

    def get_admin_url(self):
        info = (self._meta.app_label, self._meta.model_name)
        return reverse('admin:{0}_{1}_change'.format(info[0], info[1]),
                       args=(self.pk,))
