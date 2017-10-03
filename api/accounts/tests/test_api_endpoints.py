# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

from rest_framework import status

from core.tests import JWTAuthenticationTestCase
from accounts.tests.factories import (UserFactory, LandlordFactory,
                                      TenantFactory)
from accounts.models import Landlord, Tenant


class TestLandlordsEndpoint(JWTAuthenticationTestCase):
    def setUp(self):
        self.staff_user = UserFactory(is_staff=True)
        self.common_user = UserFactory(is_staff=False)

        self.staff_headers = self.get_jwt_header(
            self.staff_user.username, 'password123!')

        self.common_headers = self.get_jwt_header(
            self.common_user.username, 'password123!')

        self.landlord_one = LandlordFactory(
            first_name='George', last_name='Foreman')
        self.landlord_two = LandlordFactory(
            first_name='Ronda', last_name='Rousey')

    def test_list_landlords_as_staff(self):
        """
        Should successfully list landlords when requested by authenticated
        staff user
        """
        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.landlord_one.id,
                    'name': self.landlord_one.get_full_name(),
                    'email': self.landlord_one.email
                },
                {
                    'id': self.landlord_two.id,
                    'name': self.landlord_two.get_full_name(),
                    'email': self.landlord_two.email
                }
            ]
        }
        response = self.client.get('/api/landlords', **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_landlord_as_staff(self):
        """
        Should successfully get landlord when requested by authenticated
        staff user and provided landlord id exists
        """
        expected_data = {
            'id': self.landlord_two.id,
            'name': self.landlord_two.get_full_name(),
            'email': self.landlord_two.email
        }
        response = self.client.get(
            '/api/landlords/{}'.format(self.landlord_two.id),
            **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_inexistent_landlord_as_staff(self):
        """
        Should get a 404 when trying to get inexistent landlord
        """
        expected_data = {
            'detail': 'Not found.'
        }
        response = self.client.get(
            '/api/landlords/{}'.format('a' * 16),
            **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected_data)

    def test_update_landlord_as_staff(self):
        """
        Should successfully update landlord when requested by authenticated
        staff user
        """
        new_data = {
            'first_name': 'Jack',
            'last_name': 'Sparrow',
            'email': 'jacksparrow@email.com'
        }
        response = self.client.put(
            '/api/landlords/{}'.format(self.landlord_one.id), data=new_data,
            **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_data['id'] = self.landlord_one.id
        self.assertEqual(response.data, new_data)

    def test_partially_update_landlord_as_staff(self):
        """
        Should successfully partially update landlord when requested by
        authenticated staff user
        """
        new_data = {
            'first_name': 'Jack'
        }
        expected_data = {
            'id': self.landlord_one.id,
            'first_name': 'Jack',
            'last_name': self.landlord_one.last_name,
            'email': self.landlord_one.email
        }
        response = self.client.patch(
            '/api/landlords/{}'.format(self.landlord_one.id), data=new_data,
            **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_create_landlord_as_staff(self):
        """
        Should successfully create landlord when requested by
        authenticated staff user
        """
        new_data = {
            'first_name': 'Jack',
            'last_name': 'Sparrow',
            'email': 'jacksparrow@email.com'
        }
        response = self.client.post(
            '/api/landlords', data=new_data, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        landlord = Landlord.objects.get(first_name='Jack', last_name='Sparrow')
        new_data['id'] = landlord.id
        self.assertEqual(response.data, new_data)

        # check if it was created
        response = self.client.get('/api/landlords', **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    def test_create_landlord_missing_fields_as_staff(self):
        """
        Should get 400 when trying to create landlord with missing fields
        when requested by authenticated staff user
        """
        new_data = {
            'first_name': 'Jack',
        }
        expected = {
            'detail': ("'last_name': This field is required."
                       "'email': This field is required.")
        }
        response = self.client.post(
            '/api/landlords', data=new_data, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected)

    def test_update_landlord_missing_fields_as_staff(self):
        """
        Should get 400 when trying to update landlord with missing fields
        when requested by authenticated staff user
        """
        new_data = {
            'last_name': 'Daniels',
        }
        expected = {
            'detail': ("'first_name': This field is required.'email': "
                       "This field is required.")
        }
        response = self.client.post(
            '/api/landlords', data=new_data, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected)

    def test_search_landlord_as_staff(self):
        """
        Should get filter landlord results keeping records that match the
        search terms when requested by authenticated staff users
        """
        params = {'search': self.landlord_one.first_name}
        response = self.client.get(
            '/api/landlords', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.landlord_one.id,
                    'name': self.landlord_one.get_full_name(),
                    'email': self.landlord_one.email
                }
            ]
        }
        self.assertEqual(response.data, expected)

    def test_delete_landlord_as_staff(self):
        """
        Should delete landlord when requested by authenticated staff users
        """
        response = self.client.delete(
            '/api/landlords/{}'.format(self.landlord_one.id),
            **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get('/api/landlords', **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_list_landlords_no_pagination_as_staff(self):
        """
        Should list landlords with no pagination when given parameter and
        requested by staff user
        """
        params = {'page_size': 'none'}
        response = self.client.get(
            '/api/landlords', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = [
            {
                'id': self.landlord_one.id,
                'name': self.landlord_one.get_full_name(),
                'email': self.landlord_one.email
            },
            {
                'id': self.landlord_two.id,
                'name': self.landlord_two.get_full_name(),
                'email': self.landlord_two.email
            }
        ]
        self.assertEqual(response.data, expected_data)

    def test_list_landlords_split_in_pages_as_staff(self):
        """
        Should list landlords with pagination when given parameter and
        requested by staff user
        """
        params = {'page_size': '1'}
        response = self.client.get(
            '/api/landlords', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'count': 2,
            'next': 'http://testserver/api/landlords?page=2&page_size=1',
            'previous': None,
            'results': [
                {
                    'id': self.landlord_one.id,
                    'name': self.landlord_one.get_full_name(),
                    'email': self.landlord_one.email
                }
            ]
        }
        self.assertEqual(response.data, expected_data)

    def test_list_landlords_specific_page_as_staff(self):
        """
        Should list landlords in specific results page when given parameter
        and requested by staff user
        """
        params = {'page_size': '1', 'page': '2'}
        response = self.client.get(
            '/api/landlords', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'count': 2,
            'next': None,
            'previous': 'http://testserver/api/landlords?page_size=1',
            'results': [
                {
                    'id': self.landlord_two.id,
                    'name': self.landlord_two.get_full_name(),
                    'email': self.landlord_two.email
                }
            ]
        }
        self.assertEqual(response.data, expected_data)

    def test_list_landlords_as_common(self):
        """
        Should successfully list landlords when requested by authenticated
        common user
        """
        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.landlord_one.id,
                    'name': self.landlord_one.get_full_name(),
                    'email': self.landlord_one.email
                },
                {
                    'id': self.landlord_two.id,
                    'name': self.landlord_two.get_full_name(),
                    'email': self.landlord_two.email
                }
            ]
        }
        response = self.client.get('/api/landlords', **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_landlord_as_common(self):
        """
        Should successfully get landlord when requested by authenticated
        common user and provided landlord id exists
        """
        expected_data = {
            'id': self.landlord_two.id,
            'name': self.landlord_two.get_full_name(),
            'email': self.landlord_two.email
        }
        response = self.client.get(
            '/api/landlords/{}'.format(self.landlord_two.id),
            **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_inexistent_landlord_as_common(self):
        """
        Should get a 404 when trying to get inexistent landlord
        """
        expected_data = {
            'detail': 'Not found.'
        }
        response = self.client.get(
            '/api/landlords/{}'.format('a' * 16),
            **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected_data)

    def test_update_landlord_as_common(self):
        """
        Should successfully update landlord when requested by authenticated
        common user
        """
        new_data = {
            'first_name': 'Jack',
            'last_name': 'Sparrow',
            'email': 'jacksparrow@email.com'
        }
        response = self.client.put(
            '/api/landlords/{}'.format(self.landlord_one.id), data=new_data,
            **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_data['id'] = self.landlord_one.id
        self.assertEqual(response.data, new_data)

    def test_partially_update_landlord_as_common(self):
        """
        Should successfully partially update landlord when requested by
        authenticated common user
        """
        new_data = {
            'first_name': 'Jack'
        }
        expected_data = {
            'id': self.landlord_one.id,
            'first_name': 'Jack',
            'last_name': self.landlord_one.last_name,
            'email': self.landlord_one.email
        }
        response = self.client.patch(
            '/api/landlords/{}'.format(self.landlord_one.id), data=new_data,
            **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_create_landlord_as_common(self):
        """
        Should successfully create landlord when requested by
        authenticated common user
        """
        new_data = {
            'first_name': 'Jack',
            'last_name': 'Sparrow',
            'email': 'jacksparrow@email.com'
        }
        response = self.client.post(
            '/api/landlords', data=new_data, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        landlord = Landlord.objects.get(first_name='Jack', last_name='Sparrow')
        new_data['id'] = landlord.id
        self.assertEqual(response.data, new_data)

        # check if it was created
        response = self.client.get('/api/landlords', **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    def test_create_landlord_missing_fields_as_common(self):
        """
        Should get 400 when trying to create landlord with missing fields
        when requested by authenticated common user
        """
        new_data = {
            'first_name': 'Jack',
        }
        expected = {
            'detail': ("'last_name': This field is required."
                       "'email': This field is required.")
        }
        response = self.client.post(
            '/api/landlords', data=new_data, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected)

    def test_update_landlord_missing_fields_as_common(self):
        """
        Should get 400 when trying to update landlord with missing fields
        when requested by authenticated common user
        """
        new_data = {
            'last_name': 'Daniels',
        }
        expected = {
            'detail': ("'first_name': This field is required.'email': "
                       "This field is required.")
        }
        response = self.client.post(
            '/api/landlords', data=new_data, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected)

    def test_search_landlord_as_common(self):
        """
        Should get filter landlord results keeping records that match the
        search terms when requested by authenticated common user
        """
        params = {'search': self.landlord_one.first_name}
        response = self.client.get(
            '/api/landlords', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.landlord_one.id,
                    'name': self.landlord_one.get_full_name(),
                    'email': self.landlord_one.email
                }
            ]
        }
        self.assertEqual(response.data, expected)

    def test_delete_landlord_as_common(self):
        """
        Should get 401 when trying to delete a Landlord when requested by
        authenticated common user
        """
        response = self.client.delete(
            '/api/landlords/{}'.format(self.landlord_one.id),
            **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        expected = {'detail': ('You do not have the permission to delete '
                               'Landlords information')}
        self.assertEqual(response.data, expected)

    def test_list_landlords_no_pagination_as_common(self):
        """
        Should list landlords with no pagination when given parameter and
        requested by common user
        """
        params = {'page_size': 'none'}
        response = self.client.get(
            '/api/landlords', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = [
            {
                'id': self.landlord_one.id,
                'name': self.landlord_one.get_full_name(),
                'email': self.landlord_one.email
            },
            {
                'id': self.landlord_two.id,
                'name': self.landlord_two.get_full_name(),
                'email': self.landlord_two.email
            }
        ]
        self.assertEqual(response.data, expected_data)

    def test_list_landlords_split_in_pages_as_common(self):
        """
        Should list landlords with pagination when given parameter and
        requested by common user
        """
        params = {'page_size': '1'}
        response = self.client.get(
            '/api/landlords', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'count': 2,
            'next': 'http://testserver/api/landlords?page=2&page_size=1',
            'previous': None,
            'results': [
                {
                    'id': self.landlord_one.id,
                    'name': self.landlord_one.get_full_name(),
                    'email': self.landlord_one.email
                }
            ]
        }
        self.assertEqual(response.data, expected_data)

    def test_list_landlords_specific_page_as_common(self):
        """
        Should list landlords in specific results page when given parameter
        and requested by common user
        """
        params = {'page_size': '1', 'page': '2'}
        response = self.client.get(
            '/api/landlords', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'count': 2,
            'next': None,
            'previous': 'http://testserver/api/landlords?page_size=1',
            'results': [
                {
                    'id': self.landlord_two.id,
                    'name': self.landlord_two.get_full_name(),
                    'email': self.landlord_two.email
                }
            ]
        }
        self.assertEqual(response.data, expected_data)


class TestTenantsEndpoint(JWTAuthenticationTestCase):
    def setUp(self):
        self.staff_user = UserFactory(is_staff=True)
        self.common_user = UserFactory(is_staff=False)

        self.staff_headers = self.get_jwt_header(
            self.staff_user.username, 'password123!')

        self.common_headers = self.get_jwt_header(
            self.common_user.username, 'password123!')

        self.tenant_one = TenantFactory(
            first_name='Bill', last_name='Murray')
        self.tenant_two = TenantFactory(
            first_name='Nicole', last_name='Kidman')

    def test_list_tenants_as_staff(self):
        """
        Should successfully list tenants when requested by authenticated
        staff user
        """
        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.tenant_one.id,
                    'name': self.tenant_one.get_full_name(),
                    'email': self.tenant_one.email
                },
                {
                    'id': self.tenant_two.id,
                    'name': self.tenant_two.get_full_name(),
                    'email': self.tenant_two.email
                }
            ]
        }
        response = self.client.get('/api/tenants', **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_tenant_as_staff(self):
        """
        Should successfully get tenant when requested by authenticated
        staff user and provided tenant id exists
        """
        expected_data = {
            'id': self.tenant_two.id,
            'name': self.tenant_two.get_full_name(),
            'email': self.tenant_two.email
        }
        response = self.client.get(
            '/api/tenants/{}'.format(self.tenant_two.id),
            **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_inexistent_tenant_as_staff(self):
        """
        Should get a 404 when trying to get inexistent tenant
        """
        expected_data = {
            'detail': 'Not found.'
        }
        response = self.client.get(
            '/api/tenants/{}'.format('a' * 16),
            **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected_data)

    def test_update_landlord_as_staff(self):
        """
        Should successfully update tenant when requested by authenticated
        staff user
        """
        new_data = {
            'first_name': 'Jack',
            'last_name': 'Sparrow',
            'email': 'jacksparrow@email.com'
        }
        response = self.client.put(
            '/api/tenants/{}'.format(self.tenant_one.id), data=new_data,
            **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_data['id'] = self.tenant_one.id
        self.assertEqual(response.data, new_data)

    def test_partially_update_tenant_as_staff(self):
        """
        Should successfully partially update tenant when requested by
        authenticated staff user
        """
        new_data = {
            'first_name': 'Jack'
        }
        expected_data = {
            'id': self.tenant_one.id,
            'first_name': 'Jack',
            'last_name': self.tenant_one.last_name,
            'email': self.tenant_one.email
        }
        response = self.client.patch(
            '/api/tenants/{}'.format(self.tenant_one.id), data=new_data,
            **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_create_tenant_as_staff(self):
        """
        Should successfully create tenant when requested by
        authenticated staff user
        """
        new_data = {
            'first_name': 'Jack',
            'last_name': 'Sparrow',
            'email': 'jacksparrow@email.com'
        }
        response = self.client.post(
            '/api/tenants', data=new_data, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        tenant = Tenant.objects.get(first_name='Jack', last_name='Sparrow')
        new_data['id'] = tenant.id
        self.assertEqual(response.data, new_data)

        # check if it was created
        response = self.client.get('/api/tenants', **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    def test_create_tenant_missing_fields_as_staff(self):
        """
        Should get 400 when trying to create tenant with missing fields
        when requested by authenticated staff user
        """
        new_data = {
            'first_name': 'Jack',
        }
        expected = {
            'detail': ("'last_name': This field is required."
                       "'email': This field is required.")
        }
        response = self.client.post(
            '/api/tenants', data=new_data, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected)

    def test_update_tenant_missing_fields_as_staff(self):
        """
        Should get 400 when trying to update tenant with missing fields
        when requested by authenticated staff user
        """
        new_data = {
            'last_name': 'Daniels',
        }
        expected = {
            'detail': ("'first_name': This field is required.'email': "
                       "This field is required.")
        }
        response = self.client.post(
            '/api/tenants', data=new_data, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected)

    def test_search_tenant_as_staff(self):
        """
        Should filter tenant results keeping records that match the
        search terms when requested by authenticated staff users
        """
        params = {'search': self.tenant_one.first_name}
        response = self.client.get(
            '/api/tenants', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.tenant_one.id,
                    'name': self.tenant_one.get_full_name(),
                    'email': self.tenant_one.email
                }
            ]
        }
        self.assertEqual(response.data, expected)

    def test_delete_tenant_as_staff(self):
        """
        Should delete tenant when requested by authenticated staff users
        """
        response = self.client.delete(
            '/api/tenants/{}'.format(self.tenant_one.id),
            **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get('/api/tenants', **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_list_tenants_no_pagination_as_staff(self):
        """
        Should list tenants with no pagination when given parameter and
        requested by staff user
        """
        params = {'page_size': 'none'}
        response = self.client.get(
            '/api/tenants', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = [
            {
                'id': self.tenant_one.id,
                'name': self.tenant_one.get_full_name(),
                'email': self.tenant_one.email
            },
            {
                'id': self.tenant_two.id,
                'name': self.tenant_two.get_full_name(),
                'email': self.tenant_two.email
            }
        ]
        self.assertEqual(response.data, expected_data)

    def test_list_tenants_split_in_pages_as_staff(self):
        """
        Should list tenants with pagination when given parameter and
        requested by staff user
        """
        params = {'page_size': '1'}
        response = self.client.get(
            '/api/tenants', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'count': 2,
            'next': 'http://testserver/api/tenants?page=2&page_size=1',
            'previous': None,
            'results': [
                {
                    'id': self.tenant_one.id,
                    'name': self.tenant_one.get_full_name(),
                    'email': self.tenant_one.email
                }
            ]
        }
        self.assertEqual(response.data, expected_data)

    def test_list_tenants_specific_page_as_staff(self):
        """
        Should list tenants in specific results page when given parameter
        and requested by staff user
        """
        params = {'page_size': '1', 'page': '2'}
        response = self.client.get(
            '/api/tenants', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'count': 2,
            'next': None,
            'previous': 'http://testserver/api/tenants?page_size=1',
            'results': [
                {
                    'id': self.tenant_two.id,
                    'name': self.tenant_two.get_full_name(),
                    'email': self.tenant_two.email
                }
            ]
        }
        self.assertEqual(response.data, expected_data)

    def test_list_tenants_as_common(self):
        """
        Should successfully list tenants when requested by authenticated
        common user
        """
        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.tenant_one.id,
                    'name': self.tenant_one.get_full_name(),
                    'email': self.tenant_one.email
                },
                {
                    'id': self.tenant_two.id,
                    'name': self.tenant_two.get_full_name(),
                    'email': self.tenant_two.email
                }
            ]
        }
        response = self.client.get('/api/tenants', **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_tenant_as_common(self):
        """
        Should successfully get tenant when requested by authenticated
        common user and provided tenant id exists
        """
        expected_data = {
            'id': self.tenant_two.id,
            'name': self.tenant_two.get_full_name(),
            'email': self.tenant_two.email
        }
        response = self.client.get(
            '/api/tenants/{}'.format(self.tenant_two.id),
            **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_inexistent_tenant_as_common(self):
        """
        Should get a 404 when trying to get inexistent tenant
        """
        expected_data = {
            'detail': 'Not found.'
        }
        response = self.client.get(
            '/api/tenants/{}'.format('a' * 16),
            **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected_data)

    def test_update_tenant_as_common(self):
        """
        Should successfully update tenant when requested by authenticated
        common user
        """
        new_data = {
            'first_name': 'Jack',
            'last_name': 'Sparrow',
            'email': 'jacksparrow@email.com'
        }
        response = self.client.put(
            '/api/tenants/{}'.format(self.tenant_one.id), data=new_data,
            **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_data['id'] = self.tenant_one.id
        self.assertEqual(response.data, new_data)

    def test_partially_update_tenant_as_common(self):
        """
        Should successfully partially update tenant when requested by
        authenticated common user
        """
        new_data = {
            'first_name': 'Jack'
        }
        expected_data = {
            'id': self.tenant_one.id,
            'first_name': 'Jack',
            'last_name': self.tenant_one.last_name,
            'email': self.tenant_one.email
        }
        response = self.client.patch(
            '/api/tenants/{}'.format(self.tenant_one.id), data=new_data,
            **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_create_tenant_as_common(self):
        """
        Should successfully create tenant when requested by
        authenticated common user
        """
        new_data = {
            'first_name': 'Jack',
            'last_name': 'Sparrow',
            'email': 'jacksparrow@email.com'
        }
        response = self.client.post(
            '/api/tenants', data=new_data, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        tenant = Tenant.objects.get(first_name='Jack', last_name='Sparrow')
        new_data['id'] = tenant.id
        self.assertEqual(response.data, new_data)

        # check if it was created
        response = self.client.get('/api/tenants', **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    def test_create_tenant_missing_fields_as_common(self):
        """
        Should get 400 when trying to create tenant with missing fields
        when requested by authenticated common user
        """
        new_data = {
            'first_name': 'Jack',
        }
        expected = {
            'detail': ("'last_name': This field is required."
                       "'email': This field is required.")
        }
        response = self.client.post(
            '/api/tenants', data=new_data, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected)

    def test_update_tenant_missing_fields_as_common(self):
        """
        Should get 400 when trying to update tenant with missing fields
        when requested by authenticated common user
        """
        new_data = {
            'last_name': 'Daniels',
        }
        expected = {
            'detail': ("'first_name': This field is required.'email': "
                       "This field is required.")
        }
        response = self.client.post(
            '/api/tenants', data=new_data, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected)

    def test_search_tenant_as_common(self):
        """
        Should get filter tenant results keeping records that match the
        search terms when requested by authenticated common user
        """
        params = {'search': self.tenant_one.first_name}
        response = self.client.get(
            '/api/tenants', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.tenant_one.id,
                    'name': self.tenant_one.get_full_name(),
                    'email': self.tenant_one.email
                }
            ]
        }
        self.assertEqual(response.data, expected)

    def test_delete_tenant_as_common(self):
        """
        Should get 401 when trying to delete a Tenant when requested by
        authenticated common user
        """
        response = self.client.delete(
            '/api/tenants/{}'.format(self.tenant_one.id),
            **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        expected = {'detail': ('You do not have the permission to delete '
                               'Tenants information')}
        self.assertEqual(response.data, expected)

    def test_list_tenants_no_pagination_as_common(self):
        """
        Should list tenants with no pagination when given parameter and
        requested by common user
        """
        params = {'page_size': 'none'}
        response = self.client.get(
            '/api/tenants', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = [
            {
                'id': self.tenant_one.id,
                'name': self.tenant_one.get_full_name(),
                'email': self.tenant_one.email
            },
            {
                'id': self.tenant_two.id,
                'name': self.tenant_two.get_full_name(),
                'email': self.tenant_two.email
            }
        ]
        self.assertEqual(response.data, expected_data)

    def test_list_tenants_split_in_pages_as_common(self):
        """
        Should list tenants with pagination when given parameter and
        requested by common user
        """
        params = {'page_size': '1'}
        response = self.client.get(
            '/api/tenants', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'count': 2,
            'next': 'http://testserver/api/tenants?page=2&page_size=1',
            'previous': None,
            'results': [
                {
                    'id': self.tenant_one.id,
                    'name': self.tenant_one.get_full_name(),
                    'email': self.tenant_one.email
                }
            ]
        }
        self.assertEqual(response.data, expected_data)

    def test_list_landlords_specific_page_as_common(self):
        """
        Should list tenants in specific results page when given parameter
        and requested by common user
        """
        params = {'page_size': '1', 'page': '2'}
        response = self.client.get(
            '/api/tenants', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'count': 2,
            'next': None,
            'previous': 'http://testserver/api/tenants?page_size=1',
            'results': [
                {
                    'id': self.tenant_two.id,
                    'name': self.tenant_two.get_full_name(),
                    'email': self.tenant_two.email
                }
            ]
        }
        self.assertEqual(response.data, expected_data)
