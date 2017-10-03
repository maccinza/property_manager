# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

from rest_framework import status

from core.tests import JWTAuthenticationTestCase
from accounts.tests.factories import UserFactory
from accounts.models import Landlord
from properties.models import Property


class TestPropertyEndpoints(JWTAuthenticationTestCase):
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
        self.landlord_three = Landlord.objects.create(
            first_name='Jim', last_name='Morrison',
            email='jim@mail.com')

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
            landlord=self.landlord_three)

        self.property_four = Property.objects.create(
            street='Sherlock Grove Street',
            number='68',
            city='Cambridge',
            zip_code='CB22XRC',
            description='Fantastic place totally rebuilt.',
            beds='1',
            category='apartment',
            landlord=self.landlord_one)

    def test_list_properties_as_staff(self):
        """
        Should successfully list all properties when requested by staff user
        """

        expected_data = {
            'count': Property.objects.count(),
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.property_four.id,
                    'city': self.property_four.city,
                    'street': self.property_four.street,
                    'number': self.property_four.number,
                    'zip_code': self.property_four.zip_code,
                    'category': self.property_four.category,
                    'beds': self.property_four.beds,
                    'description': self.property_four.description,
                    'landlord': {
                        'id': self.landlord_one.id,
                        'name': self.landlord_one.get_full_name(),
                        'email': self.landlord_one.email
                    }
                },
                {
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
                {
                    'id': self.property_three.id,
                    'city': self.property_three.city,
                    'street': self.property_three.street,
                    'number': self.property_three.number,
                    'zip_code': self.property_three.zip_code,
                    'category': self.property_three.category,
                    'beds': self.property_three.beds,
                    'description': self.property_three.description,
                    'landlord': {
                        'id': self.landlord_three.id,
                        'name': self.landlord_three.get_full_name(),
                        'email': self.landlord_three.email
                    }
                },
                {
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
                }
            ]
        }
        response = self.client.get('/api/properties', **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_property_as_staff(self):
        """
        Should successfully get property info when requested by staff user and
        provided id is valid
        """

        expected_data = {
            'id': self.property_three.id,
            'city': self.property_three.city,
            'street': self.property_three.street,
            'number': self.property_three.number,
            'zip_code': self.property_three.zip_code,
            'category': self.property_three.category,
            'beds': self.property_three.beds,
            'description': self.property_three.description,
            'landlord': {
                'id': self.landlord_three.id,
                'name': self.landlord_three.get_full_name(),
                'email': self.landlord_three.email
            }
        }

        response = self.client.get(
            '/api/properties/{}'.format(self.property_three.id),
            **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_inexistent_property_as_staff(self):
        """
        Should get 404 when trying to get inexistent property when
        requested by staff user
        """
        response = self.client.get(
            '/api/properties/{}'.format('a' * 16),
            **self.staff_headers)
        expected = {'detail': 'Not found.'}
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected)

    def test_filter_property_by_city(self):
        """
        Should successfully filter property by given city when
        requested by staff user
        """
        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
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
                {
                    'id': self.property_three.id,
                    'city': self.property_three.city,
                    'street': self.property_three.street,
                    'number': self.property_three.number,
                    'zip_code': self.property_three.zip_code,
                    'category': self.property_three.category,
                    'beds': self.property_three.beds,
                    'description': self.property_three.description,
                    'landlord': {
                        'id': self.landlord_three.id,
                        'name': self.landlord_three.get_full_name(),
                        'email': self.landlord_three.email
                    }
                }
            ]
        }
        params = {'city': 'London'}
        response = self.client.get(
            '/api/properties', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_filter_property_by_landlord(self):
        """
        Should successfully filter property by given landlord id when
        requested by staff user
        """
        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.property_four.id,
                    'city': self.property_four.city,
                    'street': self.property_four.street,
                    'number': self.property_four.number,
                    'zip_code': self.property_four.zip_code,
                    'category': self.property_four.category,
                    'beds': self.property_four.beds,
                    'description': self.property_four.description,
                    'landlord': {
                        'id': self.landlord_one.id,
                        'name': self.landlord_one.get_full_name(),
                        'email': self.landlord_one.email
                    }
                },
                {
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
                }
            ]
        }
        params = {'landlord_id': self.landlord_one.id}
        response = self.client.get(
            '/api/properties', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_filter_property_by_zipcode(self):
        """
        Should successfully filter property by given zipcode when
        requested by staff user
        """
        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.property_four.id,
                    'city': self.property_four.city,
                    'street': self.property_four.street,
                    'number': self.property_four.number,
                    'zip_code': self.property_four.zip_code,
                    'category': self.property_four.category,
                    'beds': self.property_four.beds,
                    'description': self.property_four.description,
                    'landlord': {
                        'id': self.landlord_one.id,
                        'name': self.landlord_one.get_full_name(),
                        'email': self.landlord_one.email
                    }
                }
            ]
        }
        params = {'zipcode': self.property_four.zip_code}
        response = self.client.get(
            '/api/properties', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_filter_property_by_street(self):
        """
        Should successfully filter property by given street when
        requested by staff user
        """
        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.property_three.id,
                    'city': self.property_three.city,
                    'street': self.property_three.street,
                    'number': self.property_three.number,
                    'zip_code': self.property_three.zip_code,
                    'category': self.property_three.category,
                    'beds': self.property_three.beds,
                    'description': self.property_three.description,
                    'landlord': {
                        'id': self.landlord_three.id,
                        'name': self.landlord_three.get_full_name(),
                        'email': self.landlord_three.email
                    }
                }
            ]
        }
        params = {'street': self.property_three.street}
        response = self.client.get(
            '/api/properties', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_filter_property_by_category(self):
        """
        Should successfully filter property by given category when
        requested by staff user
        """
        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
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
                {
                    'id': self.property_three.id,
                    'city': self.property_three.city,
                    'street': self.property_three.street,
                    'number': self.property_three.number,
                    'zip_code': self.property_three.zip_code,
                    'category': self.property_three.category,
                    'beds': self.property_three.beds,
                    'description': self.property_three.description,
                    'landlord': {
                        'id': self.landlord_three.id,
                        'name': self.landlord_three.get_full_name(),
                        'email': self.landlord_three.email
                    }
                }
            ]
        }
        params = {'category': 'house'}
        response = self.client.get(
            '/api/properties', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_filter_property_beds_as_staff(self):
        """
        Should successfully filter property by number of beds when parameter
        is given and requested by staff user
        """
        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.property_four.id,
                    'city': self.property_four.city,
                    'street': self.property_four.street,
                    'number': self.property_four.number,
                    'zip_code': self.property_four.zip_code,
                    'category': self.property_four.category,
                    'beds': self.property_four.beds,
                    'description': self.property_four.description,
                    'landlord': {
                        'id': self.landlord_one.id,
                        'name': self.landlord_one.get_full_name(),
                        'email': self.landlord_one.email
                    }
                },
                {
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
                }
            ]
        }
        params = {'beds': '1'}
        response = self.client.get(
            '/api/properties', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_filter_property_invalid_category(self):
        """
        Should return 400 when given category is invalid and
        requested by staff user
        """
        expected_data = {'detail': 'Invalid category "invalid" for property'}
        params = {'category': 'invalid'}
        response = self.client.get(
            '/api/properties', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_filter_property_invalid_beds(self):
        """
        Should return 400 when given number of beds is invalid and
        requested by staff user
        """
        expected_data = {'detail': 'Invalid number of beds "10" for property'}
        params = {'beds': '10'}
        response = self.client.get(
            '/api/properties', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_filter_property_multiple_filter(self):
        """
        Should successfully filter property by given multiple filters when
        requested by staff user
        """
        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.property_four.id,
                    'city': self.property_four.city,
                    'street': self.property_four.street,
                    'number': self.property_four.number,
                    'zip_code': self.property_four.zip_code,
                    'category': self.property_four.category,
                    'beds': self.property_four.beds,
                    'description': self.property_four.description,
                    'landlord': {
                        'id': self.landlord_one.id,
                        'name': self.landlord_one.get_full_name(),
                        'email': self.landlord_one.email
                    }
                }
            ]
        }
        params = {
            'landlord_id': self.landlord_one.id,
            'beds': '1'
        }
        response = self.client.get(
            '/api/properties', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_properties_disabled_pagination(self):
        """
        Should successfully list all properties with no pagination when
        parameter is given and requested by staff user
        """

        expected_data = [
            {
                'id': self.property_four.id,
                'city': self.property_four.city,
                'street': self.property_four.street,
                'number': self.property_four.number,
                'zip_code': self.property_four.zip_code,
                'category': self.property_four.category,
                'beds': self.property_four.beds,
                'description': self.property_four.description,
                'landlord': {
                    'id': self.landlord_one.id,
                    'name': self.landlord_one.get_full_name(),
                    'email': self.landlord_one.email
                }
            },
            {
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
            {
                'id': self.property_three.id,
                'city': self.property_three.city,
                'street': self.property_three.street,
                'number': self.property_three.number,
                'zip_code': self.property_three.zip_code,
                'category': self.property_three.category,
                'beds': self.property_three.beds,
                'description': self.property_three.description,
                'landlord': {
                    'id': self.landlord_three.id,
                    'name': self.landlord_three.get_full_name(),
                    'email': self.landlord_three.email
                }
            },
            {
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
            }
        ]
        params = {'page_size': 'none'}
        response = self.client.get(
            '/api/properties', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_properties_split_in_pages_as_staff(self):
        """
        Should successfully list properties split in pages given parameter
        and requested by staff user
        """

        expected_data = {
            'count': 4,
            'next': 'http://testserver/api/properties?page=2&page_size=1',
            'previous': None,
            'results': [
                {
                    'id': self.property_four.id,
                    'city': self.property_four.city,
                    'street': self.property_four.street,
                    'number': self.property_four.number,
                    'zip_code': self.property_four.zip_code,
                    'category': self.property_four.category,
                    'beds': self.property_four.beds,
                    'description': self.property_four.description,
                    'landlord': {
                        'id': self.landlord_one.id,
                        'name': self.landlord_one.get_full_name(),
                        'email': self.landlord_one.email
                    }
                }
            ]
        }
        params = {'page_size': '1'}
        response = self.client.get(
            '/api/properties', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_properties_specific_page_as_staff(self):
        """
        Should successfully list properties from a page when given parameter
        and requested by staff user
        """
        expected_data = {
            'count': 4,
            'next': 'http://testserver/api/properties?page=4&page_size=1',
            'previous': 'http://testserver/api/properties?page=2&page_size=1',
            'results': [
                {
                    'id': self.property_three.id,
                    'city': self.property_three.city,
                    'street': self.property_three.street,
                    'number': self.property_three.number,
                    'zip_code': self.property_three.zip_code,
                    'category': self.property_three.category,
                    'beds': self.property_three.beds,
                    'description': self.property_three.description,
                    'landlord': {
                        'id': self.landlord_three.id,
                        'name': self.landlord_three.get_full_name(),
                        'email': self.landlord_three.email
                    }
                }
            ]
        }
        params = {'page_size': '1', 'page': 3}
        response = self.client.get(
            '/api/properties', params, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_create_property_as_staff(self):
        """
        Should successfully create property when given attributes are valid
        and requested by staff user
        """
        new_data = {
            'street': 'Riverdale Avenue',
            'number': '78',
            'city': 'South Yorkshire',
            'zip_code': 'SY79XEW',
            'description': 'Incredible property with nice location',
            'beds': '2',
            'category': 'house',
            'landlord': self.landlord_three.id
        }

        response = self.client.post(
            '/api/properties', data=new_data, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.count(), 5)

    def test_create_property_invalid_landlord_as_staff(self):
        """
        Should return 404 when trying to create property when given
        landlord does not exist and requested by staff user
        """
        new_data = {
            'street': 'Riverdale Avenue',
            'number': '78',
            'city': 'South Yorkshire',
            'zip_code': 'SY79XEW',
            'description': 'Incredible property with nice location',
            'beds': '2',
            'category': 'house',
            'landlord': 'a' * 16
        }

        response = self.client.post(
            '/api/properties', data=new_data, **self.staff_headers)
        expected_data = {
            'detail': ('Landlord with id "{}" does '
                       'not exist').format('a' * 16)
        }
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected_data)

    def test_create_property_missing_landlord_as_staff(self):
        """
        Should return 400 when trying to create property with missing
        landlord parameter and requested by staff user
        """
        new_data = {
            'street': 'Riverdale Avenue',
            'number': '78',
            'city': 'South Yorkshire',
            'zip_code': 'SY79XEW',
            'description': 'Incredible property with nice location',
            'beds': '2',
            'category': 'house'
        }

        response = self.client.post(
            '/api/properties', data=new_data, **self.staff_headers)
        expected_data = {
            'detail': 'Missing landlord parameter contaning landlord id'
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_create_property_missing_parameters_as_staff(self):
        """
        Should return 400 when trying to create property with missing
        parameters and requested by staff user
        """
        new_data = {
            'street': 'Riverdale Avenue',
            'city': 'South Yorkshire',
            'zip_code': 'SY79XEW',
            'beds': '2',
            'category': 'house',
            'landlord': self.landlord_three.id
        }

        response = self.client.post(
            '/api/properties', data=new_data, **self.staff_headers)
        expected_data = {
            'detail': ("'number': This field cannot be blank.'description': "
                       "This field cannot be blank.")
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_create_property_invalid_bed_and_category_as_staff(self):
        """
        Should return 400 when trying to create property with invalid bed and
        category parameters and requested by staff user
        """
        new_data = {
            'street': 'Riverdale Avenue',
            'number': '78',
            'city': 'South Yorkshire',
            'zip_code': 'SY79XEW',
            'description': 'Incredible property with nice location',
            'beds': '10',
            'category': 'studio',
            'landlord': self.landlord_three.id
        }

        response = self.client.post(
            '/api/properties', data=new_data, **self.staff_headers)
        expected_data = {
            'detail': ("'category': Value u'studio' is not a valid choice."
                       "'beds': Value u'10' is not a valid choice.")
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_update_property_as_staff(self):
        """
        Should successfully update property when given parameters are valid
        and requested by staff user
        """
        new_data = {
            'street': 'Riverdale Avenue',
            'number': '78',
            'city': 'South Yorkshire',
            'zip_code': 'SY79XEW',
            'description': 'Incredible property with nice location',
            'beds': '1',
            'category': 'house',
            'landlord': self.landlord_three.id
        }

        response = self.client.put(
            '/api/properties/{}'.format(self.property_three.id),
            data=new_data, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_data['id'] = self.property_three.id
        self.assertEqual(response.data, new_data)

    def test_partially_update_property_as_staff(self):
        """
        Should successfully partially update property when given parameters
        are valid and requested by staff user
        """
        new_data = {
            'street': 'Riverdale Avenue',
            'beds': '2'
        }
        expected_data = {
            'street': new_data['street'],
            'number': self.property_three.number,
            'city': self.property_three.city,
            'zip_code': self.property_three.zip_code,
            'description': self.property_three.description,
            'beds': new_data['beds'],
            'category': self.property_three.category,
            'landlord': self.landlord_three.id,
            'id': self.property_three.id
        }
        response = self.client.patch(
            '/api/properties/{}'.format(self.property_three.id),
            data=new_data, **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_delete_property__as_staff(self):
        """Should successfully delete property requested by staff user"""
        response = self.client.delete(
            '/api/properties/{}'.format(self.property_three.id),
            **self.staff_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Property.objects.count(), 3)

    def test_list_properties_as_common(self):
        """
        Should successfully list all properties when requested by common user
        """
        expected_data = {
            'count': Property.objects.count(),
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.property_four.id,
                    'city': self.property_four.city,
                    'street': self.property_four.street,
                    'number': self.property_four.number,
                    'zip_code': self.property_four.zip_code,
                    'category': self.property_four.category,
                    'beds': self.property_four.beds,
                    'description': self.property_four.description,
                    'landlord': {
                        'id': self.landlord_one.id,
                        'name': self.landlord_one.get_full_name(),
                        'email': self.landlord_one.email
                    }
                },
                {
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
                {
                    'id': self.property_three.id,
                    'city': self.property_three.city,
                    'street': self.property_three.street,
                    'number': self.property_three.number,
                    'zip_code': self.property_three.zip_code,
                    'category': self.property_three.category,
                    'beds': self.property_three.beds,
                    'description': self.property_three.description,
                    'landlord': {
                        'id': self.landlord_three.id,
                        'name': self.landlord_three.get_full_name(),
                        'email': self.landlord_three.email
                    }
                },
                {
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
                }
            ]
        }
        response = self.client.get('/api/properties', **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_property_as_common(self):
        """
        Should successfully get property info when requested by common user and
        provided id is valid
        """

        expected_data = {
            'id': self.property_three.id,
            'city': self.property_three.city,
            'street': self.property_three.street,
            'number': self.property_three.number,
            'zip_code': self.property_three.zip_code,
            'category': self.property_three.category,
            'beds': self.property_three.beds,
            'description': self.property_three.description,
            'landlord': {
                'id': self.landlord_three.id,
                'name': self.landlord_three.get_full_name(),
                'email': self.landlord_three.email
            }
        }

        response = self.client.get(
            '/api/properties/{}'.format(self.property_three.id),
            **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_inexistent_property_as_common(self):
        """
        Should get 404 when trying to get inexistent property when
        requested by common user
        """
        response = self.client.get(
            '/api/properties/{}'.format('a' * 16),
            **self.common_headers)
        expected = {'detail': 'Not found.'}
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected)

    def test_filter_property_by_city(self):
        """
        Should successfully filter property by given city when
        requested by common user
        """
        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
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
                {
                    'id': self.property_three.id,
                    'city': self.property_three.city,
                    'street': self.property_three.street,
                    'number': self.property_three.number,
                    'zip_code': self.property_three.zip_code,
                    'category': self.property_three.category,
                    'beds': self.property_three.beds,
                    'description': self.property_three.description,
                    'landlord': {
                        'id': self.landlord_three.id,
                        'name': self.landlord_three.get_full_name(),
                        'email': self.landlord_three.email
                    }
                }
            ]
        }
        params = {'city': 'London'}
        response = self.client.get(
            '/api/properties', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_filter_property_by_landlord(self):
        """
        Should successfully filter property by given landlord id when
        requested by common user
        """
        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.property_four.id,
                    'city': self.property_four.city,
                    'street': self.property_four.street,
                    'number': self.property_four.number,
                    'zip_code': self.property_four.zip_code,
                    'category': self.property_four.category,
                    'beds': self.property_four.beds,
                    'description': self.property_four.description,
                    'landlord': {
                        'id': self.landlord_one.id,
                        'name': self.landlord_one.get_full_name(),
                        'email': self.landlord_one.email
                    }
                },
                {
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
                }
            ]
        }
        params = {'landlord_id': self.landlord_one.id}
        response = self.client.get(
            '/api/properties', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_filter_property_by_zipcode(self):
        """
        Should successfully filter property by given zipcode when
        requested by common user
        """
        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.property_four.id,
                    'city': self.property_four.city,
                    'street': self.property_four.street,
                    'number': self.property_four.number,
                    'zip_code': self.property_four.zip_code,
                    'category': self.property_four.category,
                    'beds': self.property_four.beds,
                    'description': self.property_four.description,
                    'landlord': {
                        'id': self.landlord_one.id,
                        'name': self.landlord_one.get_full_name(),
                        'email': self.landlord_one.email
                    }
                }
            ]
        }
        params = {'zipcode': self.property_four.zip_code}
        response = self.client.get(
            '/api/properties', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_filter_property_by_street(self):
        """
        Should successfully filter property by given street when
        requested by common user
        """
        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.property_three.id,
                    'city': self.property_three.city,
                    'street': self.property_three.street,
                    'number': self.property_three.number,
                    'zip_code': self.property_three.zip_code,
                    'category': self.property_three.category,
                    'beds': self.property_three.beds,
                    'description': self.property_three.description,
                    'landlord': {
                        'id': self.landlord_three.id,
                        'name': self.landlord_three.get_full_name(),
                        'email': self.landlord_three.email
                    }
                }
            ]
        }
        params = {'street': self.property_three.street}
        response = self.client.get(
            '/api/properties', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_filter_property_by_category(self):
        """
        Should successfully filter property by given category when
        requested by common user
        """
        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
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
                {
                    'id': self.property_three.id,
                    'city': self.property_three.city,
                    'street': self.property_three.street,
                    'number': self.property_three.number,
                    'zip_code': self.property_three.zip_code,
                    'category': self.property_three.category,
                    'beds': self.property_three.beds,
                    'description': self.property_three.description,
                    'landlord': {
                        'id': self.landlord_three.id,
                        'name': self.landlord_three.get_full_name(),
                        'email': self.landlord_three.email
                    }
                }
            ]
        }
        params = {'category': 'house'}
        response = self.client.get(
            '/api/properties', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_filter_property_beds_as_common(self):
        """
        Should successfully filter property by number of beds when parameter
        is given and requested by common user
        """
        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.property_four.id,
                    'city': self.property_four.city,
                    'street': self.property_four.street,
                    'number': self.property_four.number,
                    'zip_code': self.property_four.zip_code,
                    'category': self.property_four.category,
                    'beds': self.property_four.beds,
                    'description': self.property_four.description,
                    'landlord': {
                        'id': self.landlord_one.id,
                        'name': self.landlord_one.get_full_name(),
                        'email': self.landlord_one.email
                    }
                },
                {
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
                }
            ]
        }
        params = {'beds': '1'}
        response = self.client.get(
            '/api/properties', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_filter_property_invalid_category(self):
        """
        Should return 400 when given category is invalid and
        requested by common user
        """
        expected_data = {'detail': 'Invalid category "invalid" for property'}
        params = {'category': 'invalid'}
        response = self.client.get(
            '/api/properties', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_filter_property_invalid_beds(self):
        """
        Should return 400 when given number of beds is invalid and
        requested by common user
        """
        expected_data = {'detail': 'Invalid number of beds "10" for property'}
        params = {'beds': '10'}
        response = self.client.get(
            '/api/properties', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_filter_property_multiple_filter(self):
        """
        Should successfully filter property by given multiple filters when
        requested by common user
        """
        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.property_four.id,
                    'city': self.property_four.city,
                    'street': self.property_four.street,
                    'number': self.property_four.number,
                    'zip_code': self.property_four.zip_code,
                    'category': self.property_four.category,
                    'beds': self.property_four.beds,
                    'description': self.property_four.description,
                    'landlord': {
                        'id': self.landlord_one.id,
                        'name': self.landlord_one.get_full_name(),
                        'email': self.landlord_one.email
                    }
                }
            ]
        }
        params = {
            'landlord_id': self.landlord_one.id,
            'beds': '1'
        }
        response = self.client.get(
            '/api/properties', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_properties_disabled_pagination(self):
        """
        Should successfully list all properties with no pagination when
        parameter is given and requested by common user
        """

        expected_data = [
            {
                'id': self.property_four.id,
                'city': self.property_four.city,
                'street': self.property_four.street,
                'number': self.property_four.number,
                'zip_code': self.property_four.zip_code,
                'category': self.property_four.category,
                'beds': self.property_four.beds,
                'description': self.property_four.description,
                'landlord': {
                    'id': self.landlord_one.id,
                    'name': self.landlord_one.get_full_name(),
                    'email': self.landlord_one.email
                }
            },
            {
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
            {
                'id': self.property_three.id,
                'city': self.property_three.city,
                'street': self.property_three.street,
                'number': self.property_three.number,
                'zip_code': self.property_three.zip_code,
                'category': self.property_three.category,
                'beds': self.property_three.beds,
                'description': self.property_three.description,
                'landlord': {
                    'id': self.landlord_three.id,
                    'name': self.landlord_three.get_full_name(),
                    'email': self.landlord_three.email
                }
            },
            {
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
            }
        ]
        params = {'page_size': 'none'}
        response = self.client.get(
            '/api/properties', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_properties_split_in_pages_as_common(self):
        """
        Should successfully list properties split in pages given parameter
        and requested by common user
        """

        expected_data = {
            'count': 4,
            'next': 'http://testserver/api/properties?page=2&page_size=1',
            'previous': None,
            'results': [
                {
                    'id': self.property_four.id,
                    'city': self.property_four.city,
                    'street': self.property_four.street,
                    'number': self.property_four.number,
                    'zip_code': self.property_four.zip_code,
                    'category': self.property_four.category,
                    'beds': self.property_four.beds,
                    'description': self.property_four.description,
                    'landlord': {
                        'id': self.landlord_one.id,
                        'name': self.landlord_one.get_full_name(),
                        'email': self.landlord_one.email
                    }
                }
            ]
        }
        params = {'page_size': '1'}
        response = self.client.get(
            '/api/properties', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_properties_specific_page_as_common(self):
        """
        Should successfully list properties from a page when given parameter
        and requested by common user
        """
        expected_data = {
            'count': 4,
            'next': 'http://testserver/api/properties?page=4&page_size=1',
            'previous': 'http://testserver/api/properties?page=2&page_size=1',
            'results': [
                {
                    'id': self.property_three.id,
                    'city': self.property_three.city,
                    'street': self.property_three.street,
                    'number': self.property_three.number,
                    'zip_code': self.property_three.zip_code,
                    'category': self.property_three.category,
                    'beds': self.property_three.beds,
                    'description': self.property_three.description,
                    'landlord': {
                        'id': self.landlord_three.id,
                        'name': self.landlord_three.get_full_name(),
                        'email': self.landlord_three.email
                    }
                }
            ]
        }
        params = {'page_size': '1', 'page': 3}
        response = self.client.get(
            '/api/properties', params, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_create_property_as_common(self):
        """
        Should successfully create property when given attributes are valid
        and requested by common user
        """
        new_data = {
            'street': 'Riverdale Avenue',
            'number': '78',
            'city': 'South Yorkshire',
            'zip_code': 'SY79XEW',
            'description': 'Incredible property with nice location',
            'beds': '2',
            'category': 'house',
            'landlord': self.landlord_three.id
        }

        response = self.client.post(
            '/api/properties', data=new_data, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.count(), 5)

    def test_create_property_invalid_landlord_as_common(self):
        """
        Should return 404 when trying to create property when given
        landlord does not exist and requested by common user
        """
        new_data = {
            'street': 'Riverdale Avenue',
            'number': '78',
            'city': 'South Yorkshire',
            'zip_code': 'SY79XEW',
            'description': 'Incredible property with nice location',
            'beds': '2',
            'category': 'house',
            'landlord': 'a' * 16
        }

        response = self.client.post(
            '/api/properties', data=new_data, **self.common_headers)
        expected_data = {
            'detail': ('Landlord with id "{}" does '
                       'not exist').format('a' * 16)
        }
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected_data)

    def test_create_property_missing_landlord_as_common(self):
        """
        Should return 400 when trying to create property with missing
        landlord parameter and requested by common user
        """
        new_data = {
            'street': 'Riverdale Avenue',
            'number': '78',
            'city': 'South Yorkshire',
            'zip_code': 'SY79XEW',
            'description': 'Incredible property with nice location',
            'beds': '2',
            'category': 'house'
        }

        response = self.client.post(
            '/api/properties', data=new_data, **self.common_headers)
        expected_data = {
            'detail': 'Missing landlord parameter contaning landlord id'
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_create_property_missing_parameters_as_common(self):
        """
        Should return 400 when trying to create property with missing
        parameters and requested by common user
        """
        new_data = {
            'street': 'Riverdale Avenue',
            'city': 'South Yorkshire',
            'zip_code': 'SY79XEW',
            'beds': '2',
            'category': 'house',
            'landlord': self.landlord_three.id
        }

        response = self.client.post(
            '/api/properties', data=new_data, **self.common_headers)
        expected_data = {
            'detail': ("'number': This field cannot be blank.'description': "
                       "This field cannot be blank.")
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_create_property_invalid_bed_and_category_as_common(self):
        """
        Should return 400 when trying to create property with invalid bed and
        category parameters and requested by common user
        """
        new_data = {
            'street': 'Riverdale Avenue',
            'number': '78',
            'city': 'South Yorkshire',
            'zip_code': 'SY79XEW',
            'description': 'Incredible property with nice location',
            'beds': '10',
            'category': 'studio',
            'landlord': self.landlord_three.id
        }

        response = self.client.post(
            '/api/properties', data=new_data, **self.common_headers)
        expected_data = {
            'detail': ("'category': Value u'studio' is not a valid choice."
                       "'beds': Value u'10' is not a valid choice.")
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def test_update_property_as_common(self):
        """
        Should successfully update property when given parameters are valid
        and requested by common user
        """
        new_data = {
            'street': 'Riverdale Avenue',
            'number': '78',
            'city': 'South Yorkshire',
            'zip_code': 'SY79XEW',
            'description': 'Incredible property with nice location',
            'beds': '1',
            'category': 'house',
            'landlord': self.landlord_three.id
        }

        response = self.client.put(
            '/api/properties/{}'.format(self.property_three.id),
            data=new_data, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_data['id'] = self.property_three.id
        self.assertEqual(response.data, new_data)

    def test_partially_update_property_as_common(self):
        """
        Should successfully partially update property when given parameters
        are valid and requested by common user
        """
        new_data = {
            'street': 'Riverdale Avenue',
            'beds': '2'
        }
        expected_data = {
            'street': new_data['street'],
            'number': self.property_three.number,
            'city': self.property_three.city,
            'zip_code': self.property_three.zip_code,
            'description': self.property_three.description,
            'beds': new_data['beds'],
            'category': self.property_three.category,
            'landlord': self.landlord_three.id,
            'id': self.property_three.id
        }
        response = self.client.patch(
            '/api/properties/{}'.format(self.property_three.id),
            data=new_data, **self.common_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_delete_property__as_common(self):
        """
        Should return 401 when trying to delete property and requested by
        common user
        """
        response = self.client.delete(
            '/api/properties/{}'.format(self.property_three.id),
            **self.common_headers)
        expected = {
            'detail': ('You do not have the permission to delete '
                       'Properties information')
        }
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, expected)
        self.assertEqual(Property.objects.count(), 4)
