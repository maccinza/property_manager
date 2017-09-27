# -*- encoding: UTF-8 -*-
from django.test import TestCase
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from properties.models import Property
from accounts.models import Tenant, Landlord
from contracts.models import Contract


class TestContract(TestCase):
    def setUp(self):
        self.landlord_one = Landlord.objects.create(
            first_name='Marcius', last_name='Augustus',
            email='maug@fake.mail', password='secretpwd')

        self.landlord_two = Landlord.objects.create(
            first_name='Aurelia', last_name='Stewart',
            email='aust@fake.mail', password='secretpwd')

        self.property_one = Property.objects.create(
            street='Baker Street', number='102', zip_code='NW16XE',
            city='London', description='Some fantanstic description',
            category='house', beds='2', landlord=self.landlord_one)

        self.property_two = Property.objects.create(
            street='First Street', number='897', zip_code='NW89XE',
            city='London', description='Another description',
            category='flat', beds='1', landlord=self.landlord_two)

        self.tenant_one = Tenant.objects.create(
            first_name='Edson', last_name='Arantes',
            email='earantes@test.com', password='abc123!')

        self.tenant_two = Tenant.objects.create(
            first_name='Ada', last_name='Lovelace',
            email='alove@test.com', password='abc123!')

        self.contract_one_data = {
            'start_date': '2017-09-25',
            'end_date': '2018-09-25',
            'property': self.property_one,
            'tenant': self.tenant_one,
            'rent': 1250.25
        }

        self.contract_two_data = {
            'start_date': '2017-10-22',
            'end_date': '2018-05-22',
            'property': self.property_two,
            'tenant': self.tenant_two,
            'rent': 875.00
        }

    def check_contract(self, values, contract):
        """Helper method for checking contract attributes"""
        for attribute, value in values.items():
            if attribute == 'start_date' or attribute == 'end_date':
                date_str = getattr(contract, attribute).strftime('%Y-%m-%d')
                self.assertEqual(date_str, value)
            else:
                self.assertEqual(getattr(contract, attribute), value)

    def test_create_contract_successfully(self):
        """
        Should successfully create Contract when all required fields are
        provided
        """
        self.assertEqual(Contract.objects.count(), 0)
        contract = Contract(**self.contract_one_data)
        contract.save()
        self.assertEqual(Contract.objects.count(), 1)
        self.check_contract(self.contract_one_data, contract)

    def test_create_contract_missing_start_date(self):
        """
        Should raise ValidationError when trying to create contract with
        missing start date
        """
        self.assertEqual(Contract.objects.count(), 0)
        del(self.contract_one_data['start_date'])
        contract = Contract(**self.contract_one_data)

        with self.assertRaises(ValidationError) as raised:
            contract.save()
        expected = {'start_date': [u'This field cannot be null.']}
        self.assertEqual(Contract.objects.count(), 0)
        self.assertEqual(raised.exception.message_dict, expected)

    def test_create_contract_missing_end_date(self):
        """
        Should raise ValidationError when trying to create contract with
        missing end date
        """
        self.assertEqual(Contract.objects.count(), 0)
        del(self.contract_one_data['end_date'])
        contract = Contract(**self.contract_one_data)

        with self.assertRaises(ValidationError) as raised:
            contract.save()
        expected = {'end_date': [u'This field cannot be null.']}
        self.assertEqual(Contract.objects.count(), 0)
        self.assertEqual(raised.exception.message_dict, expected)

    def test_create_contract_missing_rent(self):
        """
        Should raise ValidationError when trying to create contract with
        missing rent
        """
        self.assertEqual(Contract.objects.count(), 0)
        del(self.contract_one_data['rent'])
        contract = Contract(**self.contract_one_data)

        with self.assertRaises(ValidationError) as raised:
            contract.save()
        expected = {'rent': [u'This field cannot be null.']}
        self.assertEqual(Contract.objects.count(), 0)
        self.assertEqual(raised.exception.message_dict, expected)

    def test_create_contract_missing_tenant(self):
        """
        Should raise ObjectDoesNotExist when trying to create
        contract with missing tenant
        """
        self.assertEqual(Contract.objects.count(), 0)
        del(self.contract_one_data['tenant'])
        contract = Contract(**self.contract_one_data)

        with self.assertRaises(ObjectDoesNotExist) as raised:
            contract.save()
        expected = 'Contract has no tenant.'
        self.assertEqual(Contract.objects.count(), 0)
        self.assertEqual(raised.exception.message, expected)

    def test_create_contract_missing_property(self):
        """
        Should raise ObjectDoesNotExist when trying to create
        contract with missing property
        """
        self.assertEqual(Contract.objects.count(), 0)
        del(self.contract_one_data['property'])
        contract = Contract(**self.contract_one_data)

        with self.assertRaises(ObjectDoesNotExist) as raised:
            contract.save()
        expected = 'Contract has no property.'
        self.assertEqual(Contract.objects.count(), 0)
        self.assertEqual(raised.exception.message, expected)

    def test_create_contract_same_property_within_date_range(self):
        """
        Should raise ValidationError when trying to create a contract for a
        property that is already in another contract and which data range
        includes the given range
        """
        # checks db does not contain contracts
        self.assertEqual(Contract.objects.count(), 0)
        # creates a contract
        contract = Contract(**self.contract_one_data)
        contract.save()
        self.assertEqual(Contract.objects.count(), 1)

        invalid_contract_data = {
            'start_date': '2017-10-27',
            'end_date': '2018-10-27',
            'property': self.property_one,
            'tenant': self.tenant_two,
            'rent': 1000.00
        }
        expected = ('There is already another contract for this property or '
                    'for this tenant and the given dates.')
        contract = Contract(**invalid_contract_data)
        with self.assertRaises(ValidationError) as raised:
            contract.save()
        self.assertIn(expected, raised.exception.message_dict['__all__'])

    def test_create_contract_same_tenant_within_date_range(self):
        """
        Should raise ValidationError when trying to create a contract for a
        tenant that is already in another contract and which data range
        includes the given range
        """
        # checks db does not contain contracts
        self.assertEqual(Contract.objects.count(), 0)
        # creates a contract
        contract = Contract(**self.contract_one_data)
        contract.save()
        self.assertEqual(Contract.objects.count(), 1)

        invalid_contract_data = {
            'start_date': '2017-10-27',
            'end_date': '2018-10-27',
            'property': self.property_two,
            'tenant': self.tenant_one,
            'rent': 1000.00
        }
        expected = ('There is already another contract for this property or '
                    'for this tenant and the given dates.')
        contract = Contract(**invalid_contract_data)
        with self.assertRaises(ValidationError) as raised:
            contract.save()
        self.assertIn(expected, raised.exception.message_dict['__all__'])

    def test_create_contract_same_property_not_matching_dates(self):
        """
        Should successfully create a contract for a property that is already
        in another contract and which data range does not include given dates
        """
        # checks db does not contain contracts
        self.assertEqual(Contract.objects.count(), 0)
        # creates a contract
        contract = Contract(**self.contract_one_data)
        contract.save()
        self.assertEqual(Contract.objects.count(), 1)

        contract_data = {
            'start_date': '2018-11-01',
            'end_date': '2019-11-01',
            'property': self.property_one,
            'tenant': self.tenant_two,
            'rent': 1000.00
        }
        contract = Contract(**contract_data)
        contract.save()
        self.assertEqual(Contract.objects.count(), 2)

    def test_create_contract_same_tenant_not_matching_dates(self):
        """
        Should successfully create a contract for a tenant that is already
        in another contract and which data range does not include given dates
        """
        # checks db does not contain contracts
        self.assertEqual(Contract.objects.count(), 0)
        # creates a contract
        contract = Contract(**self.contract_one_data)
        contract.save()
        self.assertEqual(Contract.objects.count(), 1)

        contract_data = {
            'start_date': '2018-11-01',
            'end_date': '2019-11-01',
            'property': self.property_two,
            'tenant': self.tenant_one,
            'rent': 1000.00
        }
        contract = Contract(**contract_data)
        contract.save()
        self.assertEqual(Contract.objects.count(), 2)

    def test_filter_contract(self):
        """Should successfully filter contract by its attributes"""
        # creates contracts
        contract = Contract(**self.contract_one_data)
        contract.save()
        contract = Contract(**self.contract_two_data)
        contract.save()
        self.assertEqual(Contract.objects.count(), 2)

        # filters contract by tenant
        filtered = Contract.objects.filter(tenant=self.tenant_two)
        self.assertEqual(len(filtered), 1)
        self.check_contract(self.contract_two_data, filtered[0])

    def test_delete_contract(self):
        """Should successfully delete contract"""
        # creates contracts
        contract = Contract(**self.contract_one_data)
        contract.save()
        contract = Contract(**self.contract_two_data)
        contract.save()
        self.assertEqual(Contract.objects.count(), 2)

        # delete contract which meets condition
        Contract.objects.filter(tenant=self.tenant_one).delete()
        self.assertEqual(Contract.objects.count(), 1)
        remaining = Contract.objects.get(tenant=self.tenant_two)
        self.check_contract(self.contract_two_data, remaining)
