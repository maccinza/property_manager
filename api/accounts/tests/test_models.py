# -*- encoding: UTF-8 -*-
import factory
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.conf import settings

from accounts.models import Landlord, Tenant
from accounts.tests.factories import (UserFactory, LandlordFactory,
                                      TenantFactory)


class BaseModelChecker(TestCase):
    def check_attributes(self, attributes, obj):
        """Helper method for checking if object attributes have expected values"""
        for name, value in attributes.items():
            if name == 'password':
                self.assertTrue(obj.check_password(value))
            else:
                self.assertEqual(getattr(obj, name), value)


class TestUserModel(BaseModelChecker):

    def test_create_staff_user(self):
        """
        Should create new staff user instance when all required fields
        are provided
        """
        self.assertEqual(User.objects.count(), 0)
        params = factory.build(dict, FACTORY_CLASS=UserFactory)
        params['is_superuser'] = False
        params['is_staff'] = True
        user = User.objects.create_user(**params)
        self.assertEqual(User.objects.count(), 1)
        self.check_attributes(params, user)

    def test_create_regular_user(self):
        """
        Should create new user instance when all required fields
        are provided
        """
        self.assertEqual(User.objects.count(), 0)
        params = factory.build(dict, FACTORY_CLASS=UserFactory)
        params['is_superuser'] = False
        params['is_staff'] = False
        user = User.objects.create_user(**params)
        self.assertEqual(User.objects.count(), 1)
        self.check_attributes(params, user)

    def test_create_superuser(self):
        """
        Should create new user instance when all required fields are
        provided
        """
        self.assertEqual(User.objects.count(), 0)
        params = factory.build(dict, FACTORY_CLASS=UserFactory)
        params['is_superuser'] = True
        params['is_staff'] = True
        user = User.objects.create_user(**params)
        self.assertEqual(User.objects.count(), 1)
        self.check_attributes(params, user)

    def test_filter_user(self):
        """Should filter User by its attributes"""
        self.assertEqual(User.objects.count(), 0)
        # creates two users
        UserFactory.create(is_staff=True)
        UserFactory.create(is_staff=True)
        self.assertEqual(User.objects.count(), 2)
        filtered = User.objects.filter(first_name='Elon')
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].last_name, 'Musk')

    def test_users_uniqueness(self):
        """
        Should fail to create user with the same first name, last name, and
        email
        """
        # creates two users
        UserFactory.create()
        UserFactory.create()

        db = settings.DATABASES['default']['ENGINE']
        # tries creating user with same email, first name and last name
        with self.assertRaises(IntegrityError) as raised:
            UserFactory.create()
        if db.endswith('sqlite3'):
            expected = 'UNIQUE constraint failed: auth_user.username'
            self.assertIn(expected, raised.exception.__unicode__())
        else:
            expected = ["Duplicate entry ", "for key \'username\'"]
            for msg in expected:
                self.assertIn(msg, raised.exception.__unicode__())


class TestLandlordModel(BaseModelChecker):

    def test_create_landlord(self):
        """
        Should create new landlord instance when all required fields
        are provided
        """
        self.assertEqual(Landlord.objects.count(), 0)
        params = factory.build(dict, FACTORY_CLASS=LandlordFactory)
        landlord = Landlord.objects.create(**params)
        self.assertEqual(Landlord.objects.count(), 1)
        self.check_attributes(params, landlord)

    def test_create_missing_fields(self):
        """
        Should raise ValidationError when missing required fields in
        creation
        """
        self.assertEqual(Landlord.objects.count(), 0)
        expected_errors = {
            'email': ['This field cannot be blank.']
        }
        with self.assertRaises(ValidationError) as e:
            Landlord.objects.create()
        self.assertEqual(e.exception.message_dict, expected_errors)
        self.assertEqual(Landlord.objects.count(), 0)

    def test_landlord_uniqueness(self):
        """Should fail to create landlord with the same email"""
        # creates two landlords
        LandlordFactory.create()
        LandlordFactory.create()
        # should fail to create landlord with same name and e-mail
        expected = {'email': ['Landlord with this Email already exists.']}
        with self.assertRaises(ValidationError) as raised:
            LandlordFactory.create()
        self.assertEqual(expected, raised.exception.message_dict)

    def test_create_with_given_valid_id(self):
        """Should successfully create landlord when given id is valid"""
        self.assertEqual(Landlord.objects.count(), 0)
        hash_id = 'a' * 16
        landlord = LandlordFactory.create(id=hash_id)
        self.assertEqual(landlord.id, hash_id)
        self.assertEqual(Landlord.objects.count(), 1)

    def test_create_with_given_invalid_id(self):
        """
        Should raise ValidationError create landlord when given id
        is invalid
        """
        self.assertEqual(Landlord.objects.count(), 0)
        hash_id = 'aaabbbcccdddd#!-'
        with self.assertRaises(ValidationError) as raised:
            LandlordFactory.create(id=hash_id)
        expected = {
            'id': [('ID must be a string containing 16 alphanumeric '
                    'lowercase characters')]
        }
        self.assertEqual(raised.exception.message_dict, expected)
        self.assertEqual(Landlord.objects.count(), 0)


class TestTenantModel(BaseModelChecker):

    def test_create_tenant(self):
        """
        Should create new tenant instance when all required fields are
        provided
        """
        self.assertEqual(Tenant.objects.count(), 0)
        params = factory.build(dict, FACTORY_CLASS=TenantFactory)
        tenant = TenantFactory.create(**params)
        self.assertEqual(Tenant.objects.count(), 1)
        self.check_attributes(params, tenant)

    def test_create_missing_fields(self):
        """
        Should raise ValidationError when missing required fields in creation
        """
        self.assertEqual(Tenant.objects.count(), 0)
        expected_errors = {
            'email': ['This field cannot be blank.']
        }
        tenant = Tenant()
        with self.assertRaises(ValidationError) as e:
            tenant.save()
        self.assertEqual(e.exception.message_dict, expected_errors)
        self.assertEqual(Tenant.objects.count(), 0)

    def test_tenant_uniqueness(self):
        """Should fail to create tenant with the same email"""
        # creates two tenants
        TenantFactory.create()
        TenantFactory.create()
        # should fail to create tenant with same name and e-mail
        expected = {'email': ['Tenant with this Email already exists.']}
        with self.assertRaises(ValidationError) as raised:
            TenantFactory.create()
        self.assertEqual(expected, raised.exception.message_dict)

    def test_create_with_given_valid_id(self):
        """Should successfully create tenant when given id is valid"""
        self.assertEqual(Tenant.objects.count(), 0)
        hash_id = 'a' * 16
        tenant = TenantFactory.create(id=hash_id)
        self.assertEqual(Tenant.objects.count(), 1)
        self.assertEqual(tenant.id, hash_id)

    def test_create_with_given_invalid_id(self):
        """
        Should raise ValidationError create tenant when given id
        is invalid
        """
        self.assertEqual(Tenant.objects.count(), 0)
        hash_id = 'aaabbbcccdddd#!-'
        with self.assertRaises(ValidationError) as raised:
            TenantFactory.create(id=hash_id)
        expected = {
            'id': [('ID must be a string containing 16 alphanumeric '
                    'lowercase characters')]
        }
        self.assertEqual(raised.exception.message_dict, expected)
        self.assertEqual(Tenant.objects.count(), 0)
