# -*- encoding: UTF-8 -*-
from django.test import TestCase

from accounts.models import User, Landlord
from properties.models import Property


class TestPropertyAdmin(TestCase):
    def setUp(self):
        self.credentials = {
            'email': 'testuser@fake.mail',
            'password': 'secret!123'
        }
        first_name = 'Test'
        last_name = 'User'

        self.user = User.objects.create_user(
            email=self.credentials['email'],
            password=self.credentials['password'],
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True)

        self.landlord_one = Landlord.objects.create(
            email='landlord@fake.mail',
            password='secretpass',
            first_name='John',
            last_name='Doe'
        )

        self.landlord_two = Landlord.objects.create(
            email='yalandlord@fake.mail',
            password='secretpass',
            first_name='Jane',
            last_name='Donuts'
        )

        self.property_one = {
            'street': 'Baker Street', 'number': '102', 'zip_code': 'NW16XE',
            'city': 'London', 'description': 'Some fantanstic description',
            'category': 'house', 'beds': '2', 'landlord': self.landlord_one
        }

        self.property_two = {
            'street': 'First Street', 'number': '897', 'zip_code': 'NW89XE',
            'city': 'London', 'description': 'Another description',
            'category': 'flat', 'beds': '1', 'landlord': self.landlord_two
        }

        self.client.login(email=self.credentials['email'],
                          password=self.credentials['password'])

    def test_create_property_admin_page(self):
        """Should successfully create a property using admin interface"""

        response = self.client.get('/admin/properties/property/')
        content = response.content
        # asserts that there aren't any properties in changelist
        self.assertNotIn('table', content)
        self.assertIn(
            '<a href="/admin/properties/property/add/" class="addlink">',
            content)

        # creates the property
        payload = self.property_one
        payload['landlord'] = payload['landlord'].id
        response = self.client.post(
            '/admin/properties/property/add/', payload, follow=True)
        self.assertEqual(response.status_code, 200)

        # checks it shows in listing
        response = self.client.get('/admin/properties/property/')
        content = response.content
        self.assertIn('table', content)
        self.assertIn(self.property_one['street'], content)
        self.assertIn(self.property_one['number'], content)
        self.assertIn(self.property_one['zip_code'], content)
        self.assertIn(self.property_one['city'], content)
        self.assertIn(self.property_one['category'], content)
        self.assertIn(self.property_one['beds'], content)

    def test_search_property(self):
        """Should successfully search and find property in django admin site"""
        response = self.client.get('/admin/properties/property/')
        content = response.content
        # asserts that there aren't any properties in changelist
        self.assertNotIn('table', content)
        self.assertIn(
            '<a href="/admin/properties/property/add/" class="addlink">',
            content)

        # creates two properties
        payload = self.property_one
        payload['landlord'] = payload['landlord'].id
        response = self.client.post(
            '/admin/properties/property/add/', payload, follow=True)
        self.assertEqual(response.status_code, 200)
        payload = self.property_two
        payload['landlord'] = payload['landlord'].id
        response = self.client.post(
            '/admin/properties/property/add/', payload, follow=True)
        self.assertEqual(response.status_code, 200)

        # checks both of them show up in listing
        response = self.client.get('/admin/properties/property/')
        content = response.content
        self.assertIn('table', content)
        self.assertIn(self.property_one['street'], content)
        self.assertIn(self.property_one['zip_code'], content)
        self.assertIn(self.property_two['street'], content)
        self.assertIn(self.property_two['zip_code'], content)

        # searches for property
        response = self.client.get('/admin/properties/property/?q=Baker')
        content = response.content
        self.assertIn('table', content)
        self.assertIn(self.property_one['street'], content)
        self.assertIn(self.property_one['zip_code'], content)
        self.assertNotIn(self.property_two['street'], content)

    def test_filter_property(self):
        """Should successfully filter property in django admin site"""
        # creates two properties
        payload = self.property_one
        payload['landlord'] = payload['landlord'].id
        response = self.client.post(
            '/admin/properties/property/add/', payload, follow=True)
        self.assertEqual(response.status_code, 200)
        payload = self.property_two
        payload['landlord'] = payload['landlord'].id
        response = self.client.post(
            '/admin/properties/property/add/', payload, follow=True)
        self.assertEqual(response.status_code, 200)

        # checks both of them show up in listing
        response = self.client.get('/admin/properties/property/')
        content = response.content
        self.assertIn('table', content)
        self.assertIn(self.property_one['street'], content)
        self.assertIn(self.property_one['zip_code'], content)
        self.assertIn(self.property_two['street'], content)
        self.assertIn(self.property_two['zip_code'], content)

        # filters property
        response = self.client.get(
            '/admin/properties/property/?beds__exact=1')
        content = response.content
        self.assertIn('table', content)
        self.assertIn(self.property_two['street'], content)
        self.assertIn(self.property_two['zip_code'], content)
        self.assertNotIn(self.property_one['street'], content)
