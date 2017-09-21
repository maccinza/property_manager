# -*- encoding: UTF-8 -*-
from django.test import TestCase
from django.core.exceptions import ValidationError

from accounts.models import User, Landlord, Tenant


class TestUserModel(TestCase):

    def test_create_staff_user(self):
        """
        Should create new staff user instance when all required fields
        are provided
        """
        self.assertEqual(User.objects.count(), 0)
        user = User.objects.create_user(
            first_name='John', last_name='Snow',
            email='jsnow@test.com', password='abc123!',
            is_staff=True)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Snow')
        self.assertEqual(user.email, 'jsnow@test.com')
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_staff, True)
        self.assertTrue(user.check_password('abc123!'))

    def test_create_regular_user(self):
        """
        Should create new user instance when all required fields
        are provided
        """
        self.assertEqual(User.objects.count(), 0)
        user = User.objects.create_user(
            first_name='Luke', last_name='Skywalker',
            email='lswalker@test.com', password='abc123!')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.first_name, 'Luke')
        self.assertEqual(user.last_name, 'Skywalker')
        self.assertEqual(user.email, 'lswalker@test.com')
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_staff, False)
        self.assertTrue(user.check_password('abc123!'))

    def test_create_superuser(self):
        """
        Should create new user instance when all required fields are
        provided
        """
        self.assertEqual(User.objects.count(), 0)
        user = User.objects.create_user(
            first_name='Ayn', last_name='Rand',
            email='arand@test.com', password='abc123!', is_staff=True,
            is_superuser=True)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.first_name, 'Ayn')
        self.assertEqual(user.last_name, 'Rand')
        self.assertEqual(user.email, 'arand@test.com')
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_staff, True)
        self.assertTrue(user.check_password('abc123!'))

    def test_create_missing_fields(self):
        """
        Should raise ValidationError when missing required fields in
        creation
        """
        self.assertEqual(User.objects.count(), 0)
        expected_errors = {
            'password': ['This field cannot be blank.'],
            'email': ['This field cannot be blank.']
        }
        with self.assertRaises(ValidationError) as e:
            User.objects.create()
        self.assertEqual(e.exception.message_dict, expected_errors)
        self.assertEqual(User.objects.count(), 0)


class TestLandlordModel(TestCase):

    def test_create_landlord(self):
        """
        Should create new landlord instance when all required fields
        are provided
        """
        self.assertEqual(Landlord.objects.count(), 0)
        landlord = Landlord.objects.create_user(
            first_name='Lara', last_name='Croft',
            email='lcroft@test.com', password='abc123!')
        self.assertEqual(Landlord.objects.count(), 1)
        self.assertEqual(landlord.first_name, 'Lara')
        self.assertEqual(landlord.last_name, 'Croft')
        self.assertEqual(landlord.email, 'lcroft@test.com')
        self.assertEqual(landlord.is_active, True)
        self.assertEqual(landlord.is_superuser, False)
        self.assertEqual(landlord.is_staff, False)
        self.assertTrue(landlord.check_password('abc123!'))

    def test_create_missing_fields(self):
        """
        Should raise ValidationError when missing required fields in
        creation
        """
        self.assertEqual(Landlord.objects.count(), 0)
        expected_errors = {
            'password': ['This field cannot be blank.'],
            'email': ['This field cannot be blank.']
        }
        with self.assertRaises(ValidationError) as e:
            Landlord.objects.create()
        self.assertEqual(e.exception.message_dict, expected_errors)
        self.assertEqual(Landlord.objects.count(), 0)

    def test_create_landlord_as_staff(self):
        """
        Should create new landlord instance as regular user even
        when ordered to create as staff
        """
        self.assertEqual(Landlord.objects.count(), 0)
        landlord = Landlord.objects.create_user(
            first_name='Josh', last_name='Brolin',
            email='jbrolin@test.com', password='abc123!', is_staff=True)
        self.assertEqual(Landlord.objects.count(), 1)
        self.assertEqual(landlord.first_name, 'Josh')
        self.assertEqual(landlord.last_name, 'Brolin')
        self.assertEqual(landlord.email, 'jbrolin@test.com')
        self.assertEqual(landlord.is_active, True)
        self.assertEqual(landlord.is_superuser, False)
        self.assertEqual(landlord.is_staff, False)
        self.assertTrue(landlord.check_password('abc123!'))

    def test_create_landlord_as_superuser(self):
        """
        Should create new landlord instance as regular user even when ordered
        to create as superuser
        """
        self.assertEqual(Landlord.objects.count(), 0)
        landlord = Landlord.objects.create_user(
            first_name='Lana', last_name='Del Rey',
            email='ldrey@test.com', password='abc123!', is_staff=True,
            is_superuser=True)
        self.assertEqual(Landlord.objects.count(), 1)
        self.assertEqual(landlord.first_name, 'Lana')
        self.assertEqual(landlord.last_name, 'Del Rey')
        self.assertEqual(landlord.email, 'ldrey@test.com')
        self.assertEqual(landlord.is_active, True)
        self.assertEqual(landlord.is_superuser, False)
        self.assertEqual(landlord.is_staff, False)
        self.assertTrue(landlord.check_password('abc123!'))


class TestTenantModel(TestCase):

    def test_create_tenant(self):
        """
        Should create new tenant instance when all required fields are
        provided
        """
        self.assertEqual(Tenant.objects.count(), 0)
        tenant = Tenant.objects.create_user(
            first_name='Inspector', last_name='Gadget',
            email='igadget@test.com', password='abc123!')
        self.assertEqual(Tenant.objects.count(), 1)
        self.assertEqual(tenant.first_name, 'Inspector')
        self.assertEqual(tenant.last_name, 'Gadget')
        self.assertEqual(tenant.email, 'igadget@test.com')
        self.assertEqual(tenant.is_active, True)
        self.assertEqual(tenant.is_superuser, False)
        self.assertEqual(tenant.is_staff, False)
        self.assertTrue(tenant.check_password('abc123!'))

    def test_create_missing_fields(self):
        """
        Should raise ValidationError when missing required fields in creation
        """
        self.assertEqual(Tenant.objects.count(), 0)
        expected_errors = {
            'password': ['This field cannot be blank.'],
            'email': ['This field cannot be blank.']
        }
        with self.assertRaises(ValidationError) as e:
            Tenant.objects.create()
        self.assertEqual(e.exception.message_dict, expected_errors)
        self.assertEqual(Tenant.objects.count(), 0)

    def test_create_tenant_as_staff(self):
        """
        Should create new tenant instance as regular user even when ordered to
        create as staff
        """
        self.assertEqual(Tenant.objects.count(), 0)
        tenant = Tenant.objects.create_user(
            first_name='Terry', last_name='Crews',
            email='tcrews@test.com', password='abc123!', is_staff=True)
        self.assertEqual(Tenant.objects.count(), 1)
        self.assertEqual(tenant.first_name, 'Terry')
        self.assertEqual(tenant.last_name, 'Crews')
        self.assertEqual(tenant.email, 'tcrews@test.com')
        self.assertEqual(tenant.is_active, True)
        self.assertEqual(tenant.is_superuser, False)
        self.assertEqual(tenant.is_staff, False)
        self.assertTrue(tenant.check_password('abc123!'))

    def test_create_tenant_as_superuser(self):
        """
        Should create new tenant instance as regular user even when ordered
        to create as superuser
        """
        self.assertEqual(Tenant.objects.count(), 0)
        tenant = Tenant.objects.create_user(
            first_name='Simone', last_name='Simons',
            email='simsimons@test.com', password='abc123!', is_staff=True,
            is_superuser=True)
        self.assertEqual(Tenant.objects.count(), 1)
        self.assertEqual(tenant.first_name, 'Simone')
        self.assertEqual(tenant.last_name, 'Simons')
        self.assertEqual(tenant.email, 'simsimons@test.com')
        self.assertEqual(tenant.is_active, True)
        self.assertEqual(tenant.is_superuser, False)
        self.assertEqual(tenant.is_staff, False)
        self.assertTrue(tenant.check_password('abc123!'))
