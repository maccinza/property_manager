# -*- encoding: UTF-8 -*-
import factory
from django.test import TestCase
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from contracts.models import Contract
from contracts.tests.factories import ContractFactory


class TestContract(TestCase):
    def test_create_contract_successfully(self):
        """
        Should successfully create Contract when all required fields are
        provided
        """
        # saves related objects
        contract_data = factory.build(dict, FACTORY_CLASS=ContractFactory)
        contract_data['property'].landlord.save()
        contract_data['property'].save()
        contract_data['tenant'].save()

        self.assertEqual(Contract.objects.count(), 0)
        ContractFactory(**contract_data)
        self.assertEqual(Contract.objects.count(), 1)

    def test_create_contract_successfully_with_given_valid_id(self):
        """
        Should successfully create Contract when given id is valid
        """
        self.assertEqual(Contract.objects.count(), 0)
        contract_data = factory.build(dict, FACTORY_CLASS=ContractFactory)
        contract_data['property'].landlord.save()
        contract_data['property'].save()
        contract_data['tenant'].save()
        contract_data['id'] = 'a' * 16
        ContractFactory(**contract_data)
        self.assertEqual(Contract.objects.count(), 1)

    def test_create_contract_with_given_invalid_id(self):
        """
        Should raise ValidationError when creating Contract and given
        id is invalid
        """
        self.assertEqual(Contract.objects.count(), 0)

        contract_data = factory.build(dict, FACTORY_CLASS=ContractFactory)
        contract_data['id'] = 'aaaabbbbccccddd#'
        contract_data['property'].landlord.save()
        contract_data['property'].save()
        contract_data['tenant'].save()

        expected = {
            'id': [('ID must be a string containing 16 alphanumeric '
                    'lowercase characters')]}

        with self.assertRaises(ValidationError) as raised:
            Contract(**contract_data).save()
        self.assertEqual(raised.exception.message_dict, expected)
        self.assertEqual(Contract.objects.count(), 0)

    def test_create_contract_missing_start_date(self):
        """
        Should raise ValidationError when trying to create contract with
        missing start date
        """
        self.assertEqual(Contract.objects.count(), 0)
        contract_data = factory.build(dict, FACTORY_CLASS=ContractFactory)
        contract_data['property'].landlord.save()
        contract_data['property'].save()
        contract_data['tenant'].save()
        del(contract_data['start_date'])

        with self.assertRaises(ValidationError) as raised:
            Contract(**contract_data).save()
        expected = {'start_date': [u'This field cannot be null.']}
        self.assertEqual(Contract.objects.count(), 0)
        self.assertEqual(raised.exception.message_dict, expected)

    def test_create_contract_missing_end_date(self):
        """
        Should raise ValidationError when trying to create contract with
        missing end date
        """
        self.assertEqual(Contract.objects.count(), 0)
        contract_data = factory.build(dict, FACTORY_CLASS=ContractFactory)
        contract_data['property'].landlord.save()
        contract_data['property'].save()
        contract_data['tenant'].save()
        del(contract_data['end_date'])

        with self.assertRaises(ValidationError) as raised:
            Contract(**contract_data).save()
        expected = {'end_date': [u'This field cannot be null.']}
        self.assertEqual(Contract.objects.count(), 0)
        self.assertEqual(raised.exception.message_dict, expected)

    def test_create_contract_missing_rent(self):
        """
        Should raise ValidationError when trying to create contract with
        missing rent
        """
        self.assertEqual(Contract.objects.count(), 0)
        contract_data = factory.build(dict, FACTORY_CLASS=ContractFactory)
        contract_data['property'].landlord.save()
        contract_data['property'].save()
        contract_data['tenant'].save()
        del(contract_data['rent'])

        with self.assertRaises(ValidationError) as raised:
            Contract(**contract_data).save()
        expected = {'rent': [u'This field cannot be null.']}
        self.assertEqual(Contract.objects.count(), 0)
        self.assertEqual(raised.exception.message_dict, expected)

    def test_create_contract_missing_tenant(self):
        """
        Should raise ObjectDoesNotExist when trying to create
        contract with missing tenant
        """
        self.assertEqual(Contract.objects.count(), 0)
        contract_data = factory.build(dict, FACTORY_CLASS=ContractFactory)
        contract_data['property'].landlord.save()
        contract_data['property'].save()
        contract_data['tenant'].save()
        del(contract_data['tenant'])

        with self.assertRaises(ObjectDoesNotExist) as raised:
            Contract(**contract_data).save()
        expected = 'Contract has no tenant.'
        self.assertEqual(Contract.objects.count(), 0)
        self.assertEqual(raised.exception.message, expected)

    def test_create_contract_missing_property(self):
        """
        Should raise ObjectDoesNotExist when trying to create
        contract with missing property
        """
        self.assertEqual(Contract.objects.count(), 0)
        contract_data = factory.build(dict, FACTORY_CLASS=ContractFactory)
        contract_data['property'].landlord.save()
        contract_data['tenant'].save()
        del(contract_data['property'])

        with self.assertRaises(ObjectDoesNotExist) as raised:
            Contract(**contract_data).save()
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
        # creates contracts
        contract_one = ContractFactory()
        contract_two = ContractFactory()
        self.assertEqual(Contract.objects.count(), 2)

        invalid_contract_data = {
            'start_date': '2017-10-27',
            'end_date': '2018-10-27',
            'property': contract_one.property,
            'tenant': contract_two.tenant,
            'rent': 1000.00
        }
        expected = ('There is already another contract for this property or '
                    'for this tenant and the given dates.')
        with self.assertRaises(ValidationError) as raised:
            Contract(**invalid_contract_data).save()
        self.assertIn(expected, raised.exception.message_dict['__all__'])

    def test_create_contract_same_tenant_within_date_range(self):
        """
        Should raise ValidationError when trying to create a contract for a
        tenant that is already in another contract and which data range
        includes the given range
        """
        # checks db does not contain contracts
        self.assertEqual(Contract.objects.count(), 0)
        # creates a contracts
        contract_one = ContractFactory()
        contract_two = ContractFactory()
        self.assertEqual(Contract.objects.count(), 2)

        invalid_contract_data = {
            'start_date': '2017-10-27',
            'end_date': '2018-10-27',
            'property': contract_two.property,
            'tenant': contract_one.tenant,
            'rent': 1000.00
        }
        expected = ('There is already another contract for this property or '
                    'for this tenant and the given dates.')
        with self.assertRaises(ValidationError) as raised:
            Contract(**invalid_contract_data).save()
        self.assertIn(expected, raised.exception.message_dict['__all__'])

    def test_create_contract_same_property_not_matching_dates(self):
        """
        Should successfully create a contract for a property that is already
        in another contract and which data range does not include given dates
        """
        # checks db does not contain contracts
        self.assertEqual(Contract.objects.count(), 0)
        # creates a contract
        contract_one = ContractFactory()
        contract_two = ContractFactory()
        self.assertEqual(Contract.objects.count(), 2)

        contract_data = {
            'start_date': '2018-11-01',
            'end_date': '2019-11-01',
            'property': contract_one.property,
            'tenant': contract_two.tenant,
            'rent': 1000.00
        }
        Contract(**contract_data).save()
        self.assertEqual(Contract.objects.count(), 3)

    def test_create_contract_same_tenant_not_matching_dates(self):
        """
        Should successfully create a contract for a tenant that is already
        in another contract and which data range does not include given dates
        """
        # checks db does not contain contracts
        self.assertEqual(Contract.objects.count(), 0)
        # creates contracts
        contract_one = ContractFactory()
        contract_two = ContractFactory()
        self.assertEqual(Contract.objects.count(), 2)

        contract_data = {
            'start_date': '2018-11-01',
            'end_date': '2019-11-01',
            'property': contract_two.property,
            'tenant': contract_one.tenant,
            'rent': 1000.00
        }
        Contract(**contract_data)
        self.assertEqual(Contract.objects.count(), 2)

    def test_filter_contract(self):
        """Should successfully filter contract by its attributes"""
        # creates contracts
        ContractFactory()
        contract_two = ContractFactory()
        self.assertEqual(Contract.objects.count(), 2)

        # filters contract by tenant
        filtered = Contract.objects.filter(
            tenant=contract_two.tenant)
        self.assertEqual(len(filtered), 1)

    def test_delete_contract(self):
        """Should successfully delete contract"""
        # creates contracts
        contract_one = ContractFactory()
        contract_two = ContractFactory()
        self.assertEqual(Contract.objects.count(), 2)

        # delete contract which meets condition
        tenant = contract_one.tenant
        Contract.objects.filter(
            tenant__first_name=tenant.first_name).delete()
        self.assertEqual(Contract.objects.count(), 1)
        tenant = contract_two.tenant
        remaining = Contract.objects.get(
            tenant=tenant)
        self.assertEqual(contract_two, remaining)

    def test_create_contract_invalid_dates(self):
        """
        Should raise ValidationError when trying to create a contract for a
        with ending date smaller than starting date
        """
        # checks db does not contain contracts
        contract_one = ContractFactory()
        contract_two = ContractFactory()
        self.assertEqual(Contract.objects.count(), 2)
        invalid_contract_data = {
            'start_date': '2017-10-27',
            'end_date': '2017-01-27',
            'property': contract_one.property,
            'tenant': contract_two.tenant,
            'rent': 1000.00
        }
        expected = (u'Invalid dates for contract. Ending date should come '
                    'after starting date.')
        with self.assertRaises(ValidationError) as raised:
            Contract(**invalid_contract_data).save()
        self.assertIn(expected, raised.exception.message_dict['__all__'])

    def test_get_contract_admin_url(self):
        """Should successfully retrieve admin url for given contract"""
        contract = ContractFactory()
        expected_url = ('/admin/contracts/contract/{}/'
                        'change/').format(contract.id)
        self.assertEqual(expected_url, contract.get_admin_url())
