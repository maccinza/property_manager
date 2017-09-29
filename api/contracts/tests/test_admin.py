# -*- encoding: UTF-8 -*-
import factory
from django.test import TestCase

from accounts.models import User, Landlord
from contracts.models import Contract
from contracts.tests.factories import ContractFactory


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

        self.contract_one_data = factory.build(
            dict, FACTORY_CLASS=ContractFactory)
        self.contract_one_data['property'].landlord.save()
        self.contract_one_data['property'].save()
        self.contract_one_data['tenant'].save()

        self.contract_two_data = factory.build(
            dict, FACTORY_CLASS=ContractFactory)
        self.contract_two_data['property'].landlord.save()
        self.contract_two_data['property'].save()
        self.contract_two_data['tenant'].save()

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
        payload['tenant'] = payload['tenant'].id
        payload['property'] = payload['property'].id
        response = self.client.post(
            '/admin/contracts/contract/add/', payload, follow=True)
        self.assertEqual(response.status_code, 200)

        # checks it shows in listing
        response = self.client.get('/admin/contracts/contract/')
        content = response.content
        self.assertIn('table', content)
        self.assertIn('Sept. 25, 2017', content)
        self.assertIn('Sept. 25, 2018', content)
        self.assertIn(str(self.contract_one_data['rent']), content)

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
        payload['tenant'] = payload['tenant'].id
        payload['property'] = payload['property'].id
        response = self.client.post(
            '/admin/contracts/contract/add/', payload, follow=True)
        self.assertEqual(response.status_code, 200)
        payload = self.contract_two_data
        payload['tenant'] = payload['tenant'].id
        payload['property'] = payload['property'].id
        response = self.client.post(
            '/admin/contracts/contract/add/', payload, follow=True)
        self.assertEqual(response.status_code, 200)

        # checks both of them show up in listing
        response = self.client.get('/admin/contracts/contract/')
        content = response.content
        self.assertIn('table', content)
        self.assertIn('Sept. 25, 2017', content)
        self.assertIn('Sept. 25, 2018', content)
        self.assertIn(str(self.contract_one_data['rent']), content)
        self.assertIn('Oct. 22, 2017', content)
        self.assertIn('Sept. 22, 2018', content)
        self.assertIn(str(self.contract_two_data['rent']), content)

        # searches for contract
        contract = Contract.objects.get(
            property=self.contract_one_data['property'])

        contract_two = Contract.objects.get(
            property=self.contract_two_data['property'])
        response = self.client.get(
            '/admin/contracts/contract/?q={}'.format(
                contract.property.city))
        content = response.content
        self.assertIn('table', content)
        self.assertIn(contract.tenant.get_full_name(), content)
        self.assertIn(contract.property.__unicode__(), content)
        self.assertNotIn(contract_two.tenant.get_full_name(), content)
        self.assertNotIn(contract_two.property.__unicode__(), content)
