# -*- encoding: UTF-8 -*-
from django.test import TestCase

from accounts.models import User, Landlord, Tenant
from properties.models import Property
from contracts.models import Contract


class TestBaseAdmin(TestCase):
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

        self.tenant_one = Tenant.objects.create(
            email='tenant@fake.mail',
            password='secretpass',
            first_name='Mary',
            last_name='Jane')

        self.tenant_two = Tenant.objects.create(
            email='yatenant@fake.mail',
            password='secretpass',
            first_name='Bruce',
            last_name='Banner')

        self.property_one = Property.objects.create(
            street='Baker Street',
            number='102',
            zip_code='NW16XE',
            city='London',
            description='Some fantanstic description',
            category='house',
            beds='1',
            landlord=self.landlord_one)

        self.property_two = Property.objects.create(
            street='Second Street',
            number='300',
            zip_code='NW16ZA',
            city='South Yorkshire',
            description='Another description',
            category='flat',
            beds='2',
            landlord=self.landlord_two)

        self.contract_one_data = {
            'start_date': '2017-01-01',
            'end_date': '2017-07-01',
            'property': self.property_one.id,
            'tenant': self.tenant_one.id,
            'rent': 600.00
        }

        self.contract_two_data = {
            'start_date': '2017-05-20',
            'end_date': '2018-05-20',
            'property': self.property_two.id,
            'tenant': self.tenant_two.id,
            'rent': 895.50
        }

        self.client.login(email=self.credentials['email'],
                          password=self.credentials['password'])

    def test_create_contract_admin_page(self):
        """Should successfully create a contract and list it in admin site"""
        # asserts that there aren't any properties in changelist view
        response = self.client.get('/admin/contracts/contract/')
        content = response.content
        self.assertNotIn('table', content)
        self.assertIn(
            '<a href="/admin/contracts/contract/add/" class="addlink">',
            content)

        # creates the contract
        payload = self.contract_one_data
        response = self.client.post(
            '/admin/contracts/contract/add/', payload, follow=True)
        self.assertEqual(response.status_code, 200)

        # checks it shows in listing
        response = self.client.get('/admin/contracts/contract/')
        content = response.content
        self.assertIn('table', content)
        self.assertIn('Jan. 1, 2017', content)
        self.assertIn('July 1, 2017', content)
        self.assertIn(str(self.contract_one_data['rent']), content)
        self.assertIn(self.tenant_one.get_full_name(), content)
        self.assertIn(self.property_one.__unicode__(), content)

    def test_search_contract(self):
        """
        Should successfully search and find a contract and list it in
        admin site
        """
        response = self.client.get('/admin/contracts/contract/')
        content = response.content
        # asserts that there aren't any contracts in changelist
        self.assertNotIn('table', content)
        self.assertIn(
            '<a href="/admin/contracts/contract/add/" class="addlink">',
            content)

        # creates two contracts
        payload = self.contract_one_data
        response = self.client.post(
            '/admin/contracts/contract/add/', payload, follow=True)
        self.assertEqual(response.status_code, 200)
        payload = self.contract_two_data
        response = self.client.post(
            '/admin/contracts/contract/add/', payload, follow=True)
        self.assertEqual(response.status_code, 200)

        # checks both of them show up in listing
        response = self.client.get('/admin/contracts/contract/')
        content = response.content
        self.assertIn('table', content)
        self.assertIn('Jan. 1, 2017', content)
        self.assertIn('July 1, 2017', content)
        self.assertIn(str(self.contract_one_data['rent']), content)
        self.assertIn(self.tenant_one.get_full_name(), content)
        self.assertIn(self.property_one.__unicode__(), content)
        self.assertIn('May 20, 2017', content)
        self.assertIn('May 20, 2018', content)
        self.assertIn(str(self.contract_two_data['rent']), content)
        self.assertIn(self.tenant_two.get_full_name(), content)
        self.assertIn(self.property_two.__unicode__(), content)

        # searches for contract
        response = self.client.get('/admin/contracts/contract/?q=London')
        content = response.content
        self.assertIn('table', content)
        self.assertIn(self.tenant_one.get_full_name(), content)
        self.assertIn(self.property_one.__unicode__(), content)
        self.assertNotIn(self.tenant_two.get_full_name(), content)
        self.assertNotIn(self.property_two.__unicode__(), content)

    def test_filter_contract(self):
        """Should successfully filter contract in django admin site"""
        # creates two contracts
        payload = self.contract_one_data
        response = self.client.post(
            '/admin/contracts/contract/add/', payload, follow=True)
        self.assertEqual(response.status_code, 200)
        payload = self.contract_two_data
        response = self.client.post(
            '/admin/contracts/contract/add/', payload, follow=True)
        self.assertEqual(response.status_code, 200)

        # checks both of them show up in listing
        response = self.client.get('/admin/contracts/contract/')
        content = response.content
        self.assertIn('table', content)
        self.assertIn(self.tenant_one.get_full_name(), content)
        self.assertIn(self.property_one.__unicode__(), content)
        self.assertIn(self.tenant_two.get_full_name(), content)
        self.assertIn(self.property_two.__unicode__(), content)

        # filters contract
        response = self.client.get(
            '/admin/contracts/contract/?start_date__gte=2017-05-20'
            '&start_date__lt=2018-05-20')
        content = response.content
        self.assertIn('table', content)
        self.assertNotIn(self.tenant_one.get_full_name(), content)
        self.assertNotIn(self.property_one.__unicode__(), content)
        self.assertIn(self.tenant_two.get_full_name(), content)
        self.assertIn(self.property_two.__unicode__(), content)
