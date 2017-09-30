# -*- encoding: UTF-8 -*-
import factory
from django.test import TestCase
from django.contrib.auth.models import User

from accounts.tests.factories import LandlordFactory, TenantFactory


class TestBaseAdmin(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser@fake.mail',
            'password': 'secret!123'
        }
        first_name = 'Test'
        last_name = 'User'

        self.user = User.objects.create_user(
            username=self.credentials['username'],
            password=self.credentials['password'],
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True)

        self.landlord_one = factory.build(dict, FACTORY_CLASS=LandlordFactory)

        self.landlord_two = factory.build(dict, FACTORY_CLASS=LandlordFactory)

        self.tenant_one = factory.build(dict, FACTORY_CLASS=TenantFactory)

        self.tenant_two = factory.build(dict, FACTORY_CLASS=TenantFactory)


class TestLoginAdminView(TestBaseAdmin):

    def test_user_login(self):
        """Should successfully login a staff user into django admin site"""
        response = self.client.post('/admin/login/',
                                    {'username': self.credentials['username'],
                                     'password': self.credentials['password']},
                                    follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/profile/')

    def test_failed_login(self):
        """Should fail to login inexistent user into django admin site"""
        response = self.client.post('/admin/login/',
                                    {'username': 'john.doe@fake.mail',
                                     'password': 'whatasecret'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'Please enter the correct username and password for a staff '
            'account', response.content)

    def test_user_login_wrong_credentials(self):
        """
        Should fail to login a staff user with wrong credentials into django
        admin site
        """
        response = self.client.post('/admin/login/',
                                    {'username': self.credentials['username'],
                                     'password': 'oopsIdontknow'},
                                    follow=False)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'Please enter the correct username and password for a staff '
            'account', response.content)

    def test_access_admin_page(self):
        """
        Should successfully access the admin page with a logged in staff
        user in django admin site
        """
        self.client.login(username=self.credentials['username'],
                          password=self.credentials['password'])

        response = self.client.get('/admin/')
        content = response.content
        self.assertIn('Site administration | Django site admin', content)
        self.assertIn('<a href="/admin/accounts/landlord/">Landlords</a>',
                      content)
        self.assertIn('<a href="/admin/accounts/tenant/">Tenants</a>', content)


class TestLandlordAdminViews(TestBaseAdmin):

    def test_create_landlord_admin_page(self):
        """Should successfully create landlord in django admin site"""
        self.client.login(username=self.credentials['username'],
                          password=self.credentials['password'])

        response = self.client.get('/admin/accounts/landlord/')
        content = response.content
        # asserts that there arent any landords in changelist
        self.assertNotIn('table', content)
        self.assertIn(
            '<a href="/admin/accounts/landlord/add/" class="addlink">',
            content)

        # creates the landlord
        response = self.client.post(
            '/admin/accounts/landlord/add/', self.landlord_one, follow=True)
        self.assertEqual(response.status_code, 200)

        # checks it shows in listing
        response = self.client.get('/admin/accounts/landlord/')
        content = response.content
        self.assertIn('table', content)
        self.assertIn(self.landlord_one['first_name'], content)
        self.assertIn(self.landlord_one['last_name'], content)
        self.assertIn(self.landlord_one['email'], content)

    def test_search_landlord(self):
        """Should successfully search and find landlord in django admin site"""
        self.client.login(username=self.credentials['username'],
                          password=self.credentials['password'])

        response = self.client.get('/admin/accounts/landlord/')
        content = response.content
        # asserts that there arent any landords in changelist
        self.assertNotIn('table', content)
        self.assertIn(
            '<a href="/admin/accounts/landlord/add/" class="addlink">',
            content)

        # creates two landlords
        response = self.client.post(
            '/admin/accounts/landlord/add/', self.landlord_one, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            '/admin/accounts/landlord/add/', self.landlord_two, follow=True)
        self.assertEqual(response.status_code, 200)

        # checks both of them show up in listing
        response = self.client.get('/admin/accounts/landlord/')
        content = response.content
        self.assertIn('table', content)
        self.assertIn(self.landlord_one['first_name'], content)
        self.assertIn(self.landlord_one['last_name'], content)
        self.assertIn(self.landlord_one['email'], content)
        self.assertIn(self.landlord_two['first_name'], content)
        self.assertIn(self.landlord_two['last_name'], content)
        self.assertIn(self.landlord_two['email'], content)

        # searches for landlord
        response = self.client.get('/admin/accounts/landlord/?q={}'.format(
            self.landlord_one['first_name']))
        content = response.content
        self.assertIn('table', content)
        self.assertIn(self.landlord_one['first_name'], content)
        self.assertIn(self.landlord_one['last_name'], content)
        self.assertIn(self.landlord_one['email'], content)
        self.assertNotIn(self.landlord_two['first_name'], content)


class TestTenantAdminViews(TestBaseAdmin):

    def test_create_tenant_admin_page(self):
        """Should successfully create tenant in django admin site"""
        self.client.login(username=self.credentials['username'],
                          password=self.credentials['password'])

        response = self.client.get('/admin/accounts/tenant/')
        content = response.content
        # asserts that there aren't any landords in changelist
        self.assertNotIn('table', content)
        self.assertIn(
            '<a href="/admin/accounts/tenant/add/" class="addlink">',
            content)

        # creates the tenant
        response = self.client.post(
            '/admin/accounts/tenant/add/', self.tenant_one, follow=True)
        self.assertEqual(response.status_code, 200)

        # checks it shows in listing
        response = self.client.get('/admin/accounts/tenant/')
        content = response.content
        self.assertIn('table', content)
        self.assertIn(self.tenant_one['first_name'], content)
        self.assertIn(self.tenant_one['last_name'], content)
        self.assertIn(self.tenant_one['email'], content)

    def test_search_tenant(self):
        """Should successfully search and find tenant in django admin site"""
        self.client.login(username=self.credentials['username'],
                          password=self.credentials['password'])

        response = self.client.get('/admin/accounts/tenant/')
        content = response.content
        # asserts that there aren't any tenants in changelist
        self.assertNotIn('table', content)
        self.assertIn(
            '<a href="/admin/accounts/tenant/add/" class="addlink">',
            content)

        # creates two tenants
        response = self.client.post(
            '/admin/accounts/tenant/add/', self.tenant_one, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            '/admin/accounts/tenant/add/', self.tenant_two, follow=True)
        self.assertEqual(response.status_code, 200)

        # checks both of them show up in listing
        response = self.client.get('/admin/accounts/tenant/')
        content = response.content
        self.assertIn('table', content)
        self.assertIn(self.tenant_one['first_name'], content)
        self.assertIn(self.tenant_one['last_name'], content)
        self.assertIn(self.tenant_one['email'], content)
        self.assertIn(self.tenant_two['first_name'], content)
        self.assertIn(self.tenant_two['last_name'], content)
        self.assertIn(self.tenant_two['email'], content)

        # searches for tenant
        response = self.client.get('/admin/accounts/tenant/?q={}'.format(
            self.tenant_one['first_name']))
        content = response.content
        self.assertIn('table', content)
        self.assertIn(self.tenant_one['first_name'], content)
        self.assertIn(self.tenant_one['last_name'], content)
        self.assertIn(self.tenant_one['email'], content)
        self.assertNotIn(self.tenant_two['first_name'], content)
