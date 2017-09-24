# -*- encoding: UTF-8 -*-
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

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

    def test_filter_user(self):
        """Should filter User by its attributes"""
        self.assertEqual(User.objects.count(), 0)
        User.objects.create_user(
            first_name='Ayn', last_name='Rand',
            email='arand@test.com', password='abc123!', is_staff=True,
            is_superuser=True)
        User.objects.create_user(
            first_name='Margaret', last_name='Thatcher',
            email='mthatcher@test.com', password='abc123!', is_staff=True)
        self.assertEqual(User.objects.count(), 2)
        filtered = User.objects.filter(first_name='Margaret')
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].last_name, 'Thatcher')

    def test_manager_get_users_only(self):
        """Should get only User instances through UserManager"""
        self.assertEqual(User.objects.count(), 0)
        User.objects.create_user(
            first_name='Ayn', last_name='Rand',
            email='arand@test.com', password='abc123!', is_staff=True,
            is_superuser=True)
        Landlord.objects.create_user(
            first_name='Margaret', last_name='Thatcher',
            email='mthatcher@test.com', password='abc123!', is_staff=True)
        Tenant.objects.create_user(
            first_name='Edson', last_name='Arantes',
            email='earantes@test.com', password='abc123!', is_staff=True)
        self.assertEqual(User.objects.count(), 1)
        filtered = User.objects.all()
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].last_name, 'Rand')

    def test_users_uniqueness(self):
        """
        Should fail to create user with the same first name, last name, and
        email
        """
        # creates a user
        User.objects.create_user(
            first_name='Ayn', last_name='Rand',
            email='arand@test.com', password='abc123!', is_staff=True,
            is_superuser=True)
        # should fail to create user with same name and e-mail
        expected = ('User with this Email, First name and Last name already '
                    'exists.')
        with self.assertRaises(ValidationError) as raised:
            User.objects.create_user(
                first_name='Ayn', last_name='Rand',
                email='arand@test.com', password='abc123!', is_staff=True)
        self.assertIn(expected, raised.exception.message_dict['__all__'])


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

    def test_landlord_uniqueness(self):
        """Should fail to create landlord with the same email"""
        email = 'arand@test.com'
        # creates a user
        Landlord.objects.create_user(
            first_name='Ayn', last_name='Rand',
            email=email, password='abc123!')
        # should fail to create user with same name and e-mail
        expected = "Duplicate entry '{}' for key 'email'".format(email)
        with self.assertRaises(IntegrityError) as raised:
            Landlord.objects.create_user(
                first_name='Ayn', last_name='Rand',
                email=email, password='abc123!')
        self.assertIn(expected, raised.exception.args)


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

    def test_tenant_uniqueness(self):
        """Should fail to create tenant with the same email"""
        email = 'arand@test.com'
        # creates a user
        Tenant.objects.create_user(
            first_name='Ayn', last_name='Rand',
            email=email, password='abc123!')
        # should fail to create user with same name and e-mail
        expected = "Duplicate entry '{}' for key 'email'".format(email)
        with self.assertRaises(IntegrityError) as raised:
            Tenant.objects.create_user(
                first_name='Ayn', last_name='Rand',
                email=email, password='abc123!')
        self.assertIn(expected, raised.exception.args)
