# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

from rest_framework import status

from core.tests import JWTAuthenticationTestCase
from accounts.tests.factories import UserFactory
from accounts.models import Tenant, Landlord
from properties.models import Property
from contracts.models import Contract


class TestContractEndpoints(JWTAuthenticationTestCase):
    def setUp(self):
        self.staff_user = UserFactory(is_staff=True)
        self.common_user = UserFactory(is_staff=False)

        self.staff_headers = self.get_jwt_header(
            self.staff_user.username, 'password123!')
        self.common_headers = self.get_jwt_header(
            self.common_user.username, 'password123!')

        self.landlord_one = Landlord.objects.create(
            first_name='George', last_name='Foreman',
            email='george@mail.com')
        self.landlord_two = Landlord.objects.create(
            first_name='Ronda', last_name='Rousey',
            email='ronda@mail.com')

        self.tenant_one = Tenant.objects.create(
            first_name='George', last_name='Orwell',
            email='georgeorwell@mail.com')
        self.tenant_two = Tenant.objects.create(
            first_name='Ellen', last_name='Ripley',
            email='elripley@mail.com')
        self.tenant_three = Tenant.objects.create(
            first_name='Katniss', last_name='Everdeen',
            email='kever@mail.com')

        self.property_one = Property.objects.create(
            street='Waldo Street',
            number='100',
            city='London',
            zip_code='NW89XEZ',
            description='Amazing location',
            beds='2',
            category='house',
            landlord=self.landlord_one)

        self.property_two = Property.objects.create(
            street='Royal Gardens Avenue',
            number='190',
            city='South Yorkshire',
            zip_code='SY77XEW',
            description='Comfortable place and peaceful neighbourhood',
            beds='1',
            category='flat',
            landlord=self.landlord_two)

        self.property_three = Property.objects.create(
            street='Diagon Alley',
            number='809',
            city='London',
            zip_code='NW90XYZ',
            description=('Vibrant neighbourhood with many entertainement '
                         'options'),
            beds='4+',
            category='house',
            landlord=self.landlord_one)

        self.contract_one = Contract.objects.create(
            start_date='2017-05-01',
            end_date='2017-09-01',
            property=self.property_one,
            tenant=self.tenant_one,
            rent='1029.75')

        self.contract_two = Contract.objects.create(
            start_date='2017-10-01',
            end_date='2018-10-01',
            property=self.property_two,
            tenant=self.tenant_two,
            rent='899.99')

        self.contract_three = Contract.objects.create(
            start_date='2018-01-01',
            end_date='2019-01-01',
            property=self.property_three,
            tenant=self.tenant_three,
            rent='1223.50')

        self.all_results = [
            {
                'id': self.contract_three.id,
                'created': self.contract_three.created.strftime(
                    '%Y-%m-%d'),
                'start_date': self.contract_three.start_date.strftime(
                    '%Y-%m-%d'),
                'end_date': self.contract_three.end_date.strftime(
                    '%Y-%m-%d'),
                'rent': str(self.contract_three.rent),
                'property': {
                    'id': self.property_three.id,
                    'city': self.property_three.city,
                    'street': self.property_three.street,
                    'number': self.property_three.number,
                    'zip_code': self.property_three.zip_code,
                    'category': self.property_three.category,
                    'beds': self.property_three.beds,
                    'description': self.property_three.description,
                    'landlord': {
                        'id': self.landlord_one.id,
                        'name': self.landlord_one.get_full_name(),
                        'email': self.landlord_one.email
                    }
                },
                'tenant': {
                    'id': self.tenant_three.id,
                    'name': self.tenant_three.get_full_name(),
                    'email': self.tenant_three.email
                }
            },
            {
                'id': self.contract_two.id,
                'created': self.contract_two.created.strftime('%Y-%m-%d'),
                'start_date': self.contract_two.start_date.strftime(
                    '%Y-%m-%d'),
                'end_date': self.contract_two.end_date.strftime(
                    '%Y-%m-%d'),
                'rent': str(self.contract_two.rent),
                'property': {
                    'id': self.property_two.id,
                    'city': self.property_two.city,
                    'street': self.property_two.street,
                    'number': self.property_two.number,
                    'zip_code': self.property_two.zip_code,
                    'category': self.property_two.category,
                    'beds': self.property_two.beds,
                    'description': self.property_two.description,
                    'landlord': {
                        'id': self.landlord_two.id,
                        'name': self.landlord_two.get_full_name(),
                        'email': self.landlord_two.email
                    }
                },
                'tenant': {
                    'id': self.tenant_two.id,
                    'name': self.tenant_two.get_full_name(),
                    'email': self.tenant_two.email
                }
            },
            {
                'id': self.contract_one.id,
                'created': self.contract_one.created.strftime('%Y-%m-%d'),
                'start_date': self.contract_one.start_date.strftime(
                    '%Y-%m-%d'),
                'end_date': self.contract_one.end_date.strftime(
                    '%Y-%m-%d'),
                'rent': str(self.contract_one.rent),
                'property': {
                    'id': self.property_one.id,
                    'city': self.property_one.city,
                    'street': self.property_one.street,
                    'number': self.property_one.number,
                    'zip_code': self.property_one.zip_code,
                    'category': self.property_one.category,
                    'beds': self.property_one.beds,
                    'description': self.property_one.description,
                    'landlord': {
                        'id': self.landlord_one.id,
                        'name': self.landlord_one.get_full_name(),
                        'email': self.landlord_one.email
                    }
                },
                'tenant': {
                    'id': self.tenant_one.id,
                    'name': self.tenant_one.get_full_name(),
                    'email': self.tenant_one.email
                }
            }
        ]

    def test_list_contracts_as_staff(self):
        """
        Should successfully list all contracts when requested by staff user
        """
        expected_data = {
            'count': Contract.objects.count(),
            'next': None,
            'previous': None,
            'results': self.all_results
        }
        response = self.client.get('/api/contracts', **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_contract_as_staff(self):
        """
        Should successfully fetch contract when requested by staff user
        """
        expected_data = self.all_results[1]
        response = self.client.get(
            '/api/contracts/{}'.format(self.contract_two.id),
            **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_inexistent_contract_as_staff(self):
        """Should get 404 when trying to get inexistent contract"""
        expected_data = {
            'detail': 'Not found.'
        }
        response = self.client.get(
            '/api/contracts/{}'.format('a' * 16),
            **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected_data)

    def test_filter_contracts_by_tenant_id_as_staff(self):
        """
        Should successfully filter contracts by tenant when requested by
        staff user
        """
        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                self.all_results[0]
            ]
        }
        params = {'tenant_id': self.tenant_three.id}
        response = self.client.get(
            '/api/contracts', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_filter_contracts_by_property_id_as_staff(self):
        """
        Should successfully filter contracts by property when requested by
        staff user
        """
        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                self.all_results[0]
            ]
        }
        params = {'property_id': self.property_three.id}
        response = self.client.get(
            '/api/contracts', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_filter_contracts_by_start_date_as_staff(self):
        """
        Should successfully filter contracts by start_date when requested by
        staff user
        """
        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                self.all_results[0],
                self.all_results[1]
            ]
        }
        params = {
            'start_date': self.contract_two.start_date.strftime('%Y-%m-%d')
        }
        response = self.client.get(
            '/api/contracts', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_filter_contracts_by_end_date_as_staff(self):
        """
        Should successfully filter contracts by end_date when requested by
        staff user
        """
        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                self.all_results[2]
            ]
        }
        params = {
            'end_date': self.contract_one.end_date.strftime('%Y-%m-%d')
        }
        response = self.client.get(
            '/api/contracts', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_create_overlapping_contract_as_staff(self):
        """
        Should get 400 trying to create new contract with overlapping
        data and requested by staff user
        """
        new_data = {
            'start_date': self.contract_two.end_date.strftime(
                '%Y-%m-%d'),
            'end_date': self.contract_three.end_date.strftime(
                '%Y-%m-%d'),
            'rent': str(self.contract_three.rent),
            'property': self.property_one.id,
            'tenant': self.tenant_two.id
        }
        expected = {'detail': ("'__all__': There is already another contract "
                               "for this property or for this tenant and the "
                               "given dates.")}
        response = self.client.post(
            '/api/contracts', data=new_data, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected)

    def test_create_contract_as_staff(self):
        """
        Should successfully create new contract when requested by staff user
        """
        new_data = {
            'start_date': '2020-01-01',
            'end_date': '2021-06-01',
            'rent': str(self.contract_three.rent),
            'property': self.property_one.id,
            'tenant': self.tenant_two.id
        }
        response = self.client.post(
            '/api/contracts', data=new_data, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contract.objects.count(), 4)

    def test_create_contract_inexistent_property_as_staff(self):
        """
        Should get 404 when trying to create new contract with inexistent
        property when requested by staff user
        """
        new_data = {
            'start_date': '2020-01-01',
            'end_date': '2021-06-01',
            'rent': str(self.contract_three.rent),
            'property': 'a' * 16,
            'tenant': self.tenant_two.id
        }
        expected = {
            'detail': 'Property with id "{}" does not exist'.format('a' * 16)
        }
        response = self.client.post(
            '/api/contracts', data=new_data, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected)
        self.assertEqual(Contract.objects.count(), 3)

    def test_create_contract_missing_property_as_staff(self):
        """
        Should get 400 when trying to create new contract with missing
        property when requested by staff user
        """
        new_data = {
            'start_date': '2020-01-01',
            'end_date': '2021-06-01',
            'rent': str(self.contract_three.rent),
            'tenant': self.tenant_two.id
        }
        expected = {
            'detail': 'Missing property parameter contaning property id'
        }
        response = self.client.post(
            '/api/contracts', data=new_data, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected)
        self.assertEqual(Contract.objects.count(), 3)

    def test_create_contract_inexistent_tenant_as_staff(self):
        """
        Should get 404 when trying to create new contract with inexistent
        tenant when requested by staff user
        """
        new_data = {
            'start_date': '2020-01-01',
            'end_date': '2021-06-01',
            'rent': str(self.contract_three.rent),
            'property': self.property_three.id,
            'tenant': 'a' * 16
        }
        expected = {
            'detail': 'Tenant with id "{}" does not exist'.format('a' * 16)
        }
        response = self.client.post(
            '/api/contracts', data=new_data, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected)
        self.assertEqual(Contract.objects.count(), 3)

    def test_create_contract_missing_tenant_as_staff(self):
        """
        Should get 400 when trying to create new contract with missing
        tenant when requested by staff user
        """
        new_data = {
            'start_date': '2020-01-01',
            'end_date': '2021-06-01',
            'rent': str(self.contract_three.rent),
            'property': self.property_three.id,
        }
        expected = {
            'detail': 'Missing tenant parameter contaning tenant id'
        }
        response = self.client.post(
            '/api/contracts', data=new_data, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected)
        self.assertEqual(Contract.objects.count(), 3)

    def test_update_contract_as_staff(self):
        """
        Should successfully update contract when requested by staff user
        """
        new_data = {
            'start_date': '2020-01-01',
            'end_date': '2021-06-01',
            'rent': '2000.00',
            'property': self.property_three.id,
            'tenant': self.tenant_three.id
        }
        expected = {
            'id': self.contract_three.id,
            'created': self.contract_three.created.strftime(
                '%Y-%m-%d'),
            'start_date': '2020-01-01',
            'end_date': '2021-06-01',
            'rent': '2000.00',
            'property': self.property_three.id,
            'tenant': self.tenant_three.id
        }
        response = self.client.put(
            '/api/contracts/{}'.format(self.contract_three.id),
            data=new_data, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_update_contract_missing_fields_as_staff(self):
        """
        Should get 400 when trying to update contract with missing fields when
        requested by staff user
        """
        new_data = {
            'start_date': '2020-01-01'
        }
        expected = {
            'detail': ("'rent': This field is required.'end_date': This "
                       "field is required.")}

        response = self.client.put(
            '/api/contracts/{}'.format(self.contract_three.id),
            data=new_data, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected)

    def test_partial_update_contract_as_staff(self):
        """
        Should successfully partially update contract when requested by
        staff user
        """
        new_data = {
            'end_date': '2020-01-01'
        }
        expected = {
            'id': self.contract_three.id,
            'created': self.contract_three.created.strftime(
                '%Y-%m-%d'),
            'start_date': self.contract_three.start_date.strftime('%Y-%m-%d'),
            'end_date': '2020-01-01',
            'rent': str(self.contract_three.rent),
            'property': self.property_three.id,
            'tenant': self.tenant_three.id
        }
        response = self.client.patch(
            '/api/contracts/{}'.format(self.contract_three.id),
            data=new_data, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_delete_contract_as_staff(self):
        """
        Should successfully delete contract when requested by staff user
        """
        response = self.client.delete(
            '/api/contracts/{}'.format(self.contract_three.id),
            **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contract.objects.count(), 2)

    def test_list_contracts_disabled_pagination_as_staff(self):
        """
        Should successfully list contracts with disabled pagination when
        requested by staff user
        """
        expected = self.all_results
        params = {'page_size': 'none'}
        response = self.client.get(
            '/api/contracts', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_list_contracts_split_pages_as_staff(self):
        """
        Should successfully list contracts in split pages when
        requested by staff user
        """
        expected = {
            'count': Contract.objects.count(),
            'next': 'http://testserver/api/contracts?page=2&page_size=1',
            'previous': None,
            'results': [
                self.all_results[0]
            ]
        }
        params = {'page_size': '1'}
        response = self.client.get(
            '/api/contracts', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_list_contracts_specific_page_as_staff(self):
        """
        Should successfully list contracts in split pages showing specific
        page when requested by staff user
        """
        expected = {
            'count': Contract.objects.count(),
            'next': 'http://testserver/api/contracts?page=3&page_size=1',
            'previous': 'http://testserver/api/contracts?page_size=1',
            'results': [
                self.all_results[1]
            ]
        }
        params = {'page_size': '1', 'page': '2'}
        response = self.client.get(
            '/api/contracts', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_list_contracts_as_common(self):
        """
        Should successfully list all contracts when requested by common user
        """
        expected_data = {
            'count': Contract.objects.count(),
            'next': None,
            'previous': None,
            'results': self.all_results
        }
        response = self.client.get('/api/contracts', **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_contract_as_common(self):
        """
        Should successfully fetch contract when requested by common user
        """
        expected_data = self.all_results[1]
        response = self.client.get(
            '/api/contracts/{}'.format(self.contract_two.id),
            **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_inexistent_contract_as_common(self):
        """Should get 404 when trying to get inexistent contract"""
        expected_data = {
            'detail': 'Not found.'
        }
        response = self.client.get(
            '/api/contracts/{}'.format('a' * 16),
            **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected_data)

    def test_filter_contracts_by_tenant_id_as_common(self):
        """
        Should successfully filter contracts by tenant when requested by
        common user
        """
        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                self.all_results[0]
            ]
        }
        params = {'tenant_id': self.tenant_three.id}
        response = self.client.get(
            '/api/contracts', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_filter_contracts_by_property_id_as_common(self):
        """
        Should successfully filter contracts by property when requested by
        common user
        """
        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                self.all_results[0]
            ]
        }
        params = {'property_id': self.property_three.id}
        response = self.client.get(
            '/api/contracts', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_filter_contracts_by_start_date_as_common(self):
        """
        Should successfully filter contracts by start_date when requested by
        common user
        """
        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                self.all_results[0],
                self.all_results[1]
            ]
        }
        params = {
            'start_date': self.contract_two.start_date.strftime('%Y-%m-%d')
        }
        response = self.client.get(
            '/api/contracts', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_filter_contracts_by_end_date_as_common(self):
        """
        Should successfully filter contracts by end_date when requested by
        common user
        """
        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                self.all_results[2]
            ]
        }
        params = {
            'end_date': self.contract_one.end_date.strftime('%Y-%m-%d')
        }
        response = self.client.get(
            '/api/contracts', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_create_overlapping_contract_as_common(self):
        """
        Should get 400 trying to create new contract with overlapping
        data and requested by common user
        """
        new_data = {
            'start_date': self.contract_two.end_date.strftime(
                '%Y-%m-%d'),
            'end_date': self.contract_three.end_date.strftime(
                '%Y-%m-%d'),
            'rent': str(self.contract_three.rent),
            'property': self.property_one.id,
            'tenant': self.tenant_two.id
        }
        expected = {'detail': ("'__all__': There is already another contract "
                               "for this property or for this tenant and the "
                               "given dates.")}
        response = self.client.post(
            '/api/contracts', data=new_data, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected)

    def test_create_contract_as_common(self):
        """
        Should successfully create new contract when requested by common user
        """
        new_data = {
            'start_date': '2020-01-01',
            'end_date': '2021-06-01',
            'rent': str(self.contract_three.rent),
            'property': self.property_one.id,
            'tenant': self.tenant_two.id
        }
        response = self.client.post(
            '/api/contracts', data=new_data, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contract.objects.count(), 4)

    def test_create_contract_inexistent_property_as_common(self):
        """
        Should get 404 when trying to create new contract with inexistent
        property when requested by common user
        """
        new_data = {
            'start_date': '2020-01-01',
            'end_date': '2021-06-01',
            'rent': str(self.contract_three.rent),
            'property': 'a' * 16,
            'tenant': self.tenant_two.id
        }
        expected = {
            'detail': 'Property with id "{}" does not exist'.format('a' * 16)
        }
        response = self.client.post(
            '/api/contracts', data=new_data, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected)
        self.assertEqual(Contract.objects.count(), 3)

    def test_create_contract_missing_property_as_common(self):
        """
        Should get 400 when trying to create new contract with missing
        property when requested by common user
        """
        new_data = {
            'start_date': '2020-01-01',
            'end_date': '2021-06-01',
            'rent': str(self.contract_three.rent),
            'tenant': self.tenant_two.id
        }
        expected = {
            'detail': 'Missing property parameter contaning property id'
        }
        response = self.client.post(
            '/api/contracts', data=new_data, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected)
        self.assertEqual(Contract.objects.count(), 3)

    def test_create_contract_inexistent_tenant_as_common(self):
        """
        Should get 404 when trying to create new contract with inexistent
        tenant when requested by common user
        """
        new_data = {
            'start_date': '2020-01-01',
            'end_date': '2021-06-01',
            'rent': str(self.contract_three.rent),
            'property': self.property_three.id,
            'tenant': 'a' * 16
        }
        expected = {
            'detail': 'Tenant with id "{}" does not exist'.format('a' * 16)
        }
        response = self.client.post(
            '/api/contracts', data=new_data, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected)
        self.assertEqual(Contract.objects.count(), 3)

    def test_create_contract_missing_tenant_as_common(self):
        """
        Should get 400 when trying to create new contract with missing
        tenant when requested by common user
        """
        new_data = {
            'start_date': '2020-01-01',
            'end_date': '2021-06-01',
            'rent': str(self.contract_three.rent),
            'property': self.property_three.id,
        }
        expected = {
            'detail': 'Missing tenant parameter contaning tenant id'
        }
        response = self.client.post(
            '/api/contracts', data=new_data, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected)
        self.assertEqual(Contract.objects.count(), 3)

    def test_update_contract_as_common(self):
        """
        Should successfully update contract when requested by common user
        """
        new_data = {
            'start_date': '2020-01-01',
            'end_date': '2021-06-01',
            'rent': '2000.00',
            'property': self.property_three.id,
            'tenant': self.tenant_three.id
        }
        expected = {
            'id': self.contract_three.id,
            'created': self.contract_three.created.strftime(
                '%Y-%m-%d'),
            'start_date': '2020-01-01',
            'end_date': '2021-06-01',
            'rent': '2000.00',
            'property': self.property_three.id,
            'tenant': self.tenant_three.id
        }
        response = self.client.put(
            '/api/contracts/{}'.format(self.contract_three.id),
            data=new_data, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_update_contract_missing_fields_as_common(self):
        """
        Should get 400 when trying to update contract with missing fields when
        requested by common user
        """
        new_data = {
            'start_date': '2020-01-01'
        }
        expected = {
            'detail': ("'rent': This field is required.'end_date': This "
                       "field is required.")}

        response = self.client.put(
            '/api/contracts/{}'.format(self.contract_three.id),
            data=new_data, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected)

    def test_partial_update_contract_as_common(self):
        """
        Should successfully partially update contract when requested by
        common user
        """
        new_data = {
            'end_date': '2020-01-01'
        }
        expected = {
            'id': self.contract_three.id,
            'created': self.contract_three.created.strftime(
                '%Y-%m-%d'),
            'start_date': self.contract_three.start_date.strftime('%Y-%m-%d'),
            'end_date': '2020-01-01',
            'rent': str(self.contract_three.rent),
            'property': self.property_three.id,
            'tenant': self.tenant_three.id
        }
        response = self.client.patch(
            '/api/contracts/{}'.format(self.contract_three.id),
            data=new_data, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_delete_contract_as_common(self):
        """
        Should get 401 when trying to delete contract when
        requested by common user
        """
        expected = {
            'detail': ('You do not have the permission to delete '
                       'Contracts information')
        }
        response = self.client.delete(
            '/api/contracts/{}'.format(self.contract_three.id),
            **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, expected)
        self.assertEqual(Contract.objects.count(), 3)

    def test_list_contracts_disabled_pagination_as_common(self):
        """
        Should successfully list contracts with disabled pagination when
        requested by common user
        """
        expected = self.all_results
        params = {'page_size': 'none'}
        response = self.client.get(
            '/api/contracts', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_list_contracts_split_pages_as_common(self):
        """
        Should successfully list contracts in split pages when
        requested by common user
        """
        expected = {
            'count': Contract.objects.count(),
            'next': 'http://testserver/api/contracts?page=2&page_size=1',
            'previous': None,
            'results': [
                self.all_results[0]
            ]
        }
        params = {'page_size': '1'}
        response = self.client.get(
            '/api/contracts', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_list_contracts_specific_page_as_common(self):
        """
        Should successfully list contracts in split pages showing specific
        page when requested by common user
        """
        expected = {
            'count': Contract.objects.count(),
            'next': 'http://testserver/api/contracts?page=3&page_size=1',
            'previous': 'http://testserver/api/contracts?page_size=1',
            'results': [
                self.all_results[1]
            ]
        }
        params = {'page_size': '1', 'page': '2'}
        response = self.client.get(
            '/api/contracts', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)


