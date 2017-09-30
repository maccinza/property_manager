# -*- encoding: UTF-8 -*-
import factory
from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Landlord
from properties.tests.factories import PropertyFactory


class TestPropertyAdmin(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret!123'
        }
        first_name = 'Test'
        last_name = 'User'

        self.user = User.objects.create_user(
            username=self.credentials['username'],
            email='test@email.com',
            password=self.credentials['password'],
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True)

        self.property_one = factory.build(
            dict, FACTORY_CLASS=PropertyFactory)
        self.property_one['landlord'].save()

        self.property_two = factory.build(
            dict, FACTORY_CLASS=PropertyFactory)
        self.property_two['landlord'].save()

        self.client.login(username=self.credentials['username'],
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
        landlord = Landlord.objects.get(id=self.property_one['landlord'])
        response = self.client.get(
            '/admin/properties/property/?q={}'.format(landlord.first_name))
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
            '/admin/properties/property/?beds__exact={}'.format(
                self.property_two['beds']))
        content = response.content
        self.assertIn('table', content)
        self.assertIn(self.property_two['street'], content)
        self.assertIn(self.property_two['zip_code'], content)
        self.assertNotIn(self.property_one['street'], content)
