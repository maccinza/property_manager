# -*- encoding: UTF-8 -*-
from django.test import TestCase
from django.core.exceptions import ValidationError

from properties.models import Property
from accounts.models import Landlord


class TestProperty(TestCase):
    def setUp(self):
        self.landlord_one = Landlord.objects.create(
            first_name='Marcius', last_name='Augustus',
            email='maug@fake.mail', password='secretpwd')

        self.landlord_two = Landlord.objects.create(
            first_name='Aurelia', last_name='Stewart',
            email='aust@fake.mail', password='secretpwd')

        self.prop_values_one = {
            'street': 'Baker Street', 'number': '102', 'zip_code': 'NW16XE',
            'city': 'London', 'description': 'Some fantanstic description',
            'category': 'house', 'beds': '2', 'landlord': self.landlord_one
        }

        self.prop_values_two = {
            'street': 'First Street', 'number': '897', 'zip_code': 'NW89XE',
            'city': 'London', 'description': 'Another description',
            'category': 'flat', 'beds': '1', 'landlord': self.landlord_two
        }

    def test_create_property_successfully(self):
        """Should successfully create a Property"""
        # asserts that are no properties in db
        self.assertEqual(Property.objects.count(), 0)

        # creates property
        prop = Property.objects.create(**self.prop_values_one)

        # asserts there is a property in db
        self.assertEqual(Property.objects.count(), 1)
        # asserts created property contains the given values
        for name, value in self.prop_values_one.items():
            self.assertEqual(value, getattr(prop, name))

    def test_create_property_missing_street(self):
        """
        Should raise ValidationError when trying to create Property with
        missing or empty street value
        """
        # removes street from parameters
        del(self.prop_values_one['street'])
        # asserts there aren't Properties in db
        self.assertEqual(Property.objects.count(), 0)

        # should raise validation error when trying to create property
        # with missing street value
        expected = {'street': [u'This field cannot be blank.']}
        with self.assertRaises(ValidationError) as raised:
            Property.objects.create(**self.prop_values_one)
        self.assertEqual(raised.exception.message_dict, expected)
        self.assertEqual(Property.objects.count(), 0)

        # should raise validation error when trying to create property
        # with empty street value
        self.prop_values_one['street'] = ''
        with self.assertRaises(ValidationError) as raised:
            Property.objects.create(**self.prop_values_one)
        self.assertEqual(raised.exception.message_dict, expected)

    def test_create_property_missing_number(self):
        """
        Should raise ValidationError when trying to create Property with
        missing or empty number value
        """
        # removes number from parameters
        del(self.prop_values_one['number'])
        # asserts there aren't Properties in db
        self.assertEqual(Property.objects.count(), 0)

        # should raise validation error when trying to create property
        # with missing number value
        expected = {'number': [u'This field cannot be blank.']}
        with self.assertRaises(ValidationError) as raised:
            Property.objects.create(**self.prop_values_one)
        self.assertEqual(raised.exception.message_dict, expected)
        self.assertEqual(Property.objects.count(), 0)

        # should raise validation error when trying to create property
        # with empty number value
        self.prop_values_one['number'] = ''
        with self.assertRaises(ValidationError) as raised:
            Property.objects.create(**self.prop_values_one)
        self.assertEqual(raised.exception.message_dict, expected)

    def test_create_property_missing_zipcode(self):
        """
        Should raise ValidationError when trying to create Property with
        missing or empty zip_code value
        """
        # removes zip_code from parameters
        del(self.prop_values_one['zip_code'])
        # asserts there aren't Properties in db
        self.assertEqual(Property.objects.count(), 0)

        # should raise validation error when trying to create property
        # with missing zip_code value
        expected = {'zip_code': [u'This field cannot be blank.']}
        with self.assertRaises(ValidationError) as raised:
            Property.objects.create(**self.prop_values_one)
        self.assertEqual(raised.exception.message_dict, expected)
        self.assertEqual(Property.objects.count(), 0)

        # should raise validation error when trying to create property
        # with empty zip_code value
        self.prop_values_one['zip_code'] = ''
        with self.assertRaises(ValidationError) as raised:
            Property.objects.create(**self.prop_values_one)
        self.assertEqual(raised.exception.message_dict, expected)

    def test_create_property_missing_city(self):
        """
        Should raise ValidationError when trying to create Property with
        missing or empty city value
        """
        # removes city from parameters
        del(self.prop_values_one['city'])
        # asserts there aren't Properties in db
        self.assertEqual(Property.objects.count(), 0)

        # should raise validation error when trying to create property
        # with missing city value
        expected = {'city': [u'This field cannot be blank.']}
        with self.assertRaises(ValidationError) as raised:
            Property.objects.create(**self.prop_values_one)
        self.assertEqual(raised.exception.message_dict, expected)
        self.assertEqual(Property.objects.count(), 0)

        # should raise validation error when trying to create property
        # with empty city value
        self.prop_values_one['city'] = ''
        with self.assertRaises(ValidationError) as raised:
            Property.objects.create(**self.prop_values_one)
        self.assertEqual(raised.exception.message_dict, expected)

    def test_create_property_missing_description(self):
        """
        Should raise ValidationError when trying to create Property with
        missing or empty description value
        """
        # removes description from parameters
        del(self.prop_values_one['description'])
        # asserts there aren't Properties in db
        self.assertEqual(Property.objects.count(), 0)

        # should raise validation error when trying to create property
        # with missing description value
        expected = {'description': [u'This field cannot be blank.']}
        with self.assertRaises(ValidationError) as raised:
            Property.objects.create(**self.prop_values_one)
        self.assertEqual(raised.exception.message_dict, expected)
        self.assertEqual(Property.objects.count(), 0)

        # should raise validation error when trying to create property
        # with empty description value
        self.prop_values_one['description'] = ''
        with self.assertRaises(ValidationError) as raised:
            Property.objects.create(**self.prop_values_one)
        self.assertEqual(raised.exception.message_dict, expected)

    def test_create_property_missing_category(self):
        """
        Should create Property with default value when category is missing
        """
        # removes category from parameters
        del(self.prop_values_one['category'])
        # asserts there aren't Properties in db
        self.assertEqual(Property.objects.count(), 0)

        # should create Property with default category value
        prop = Property.objects.create(**self.prop_values_one)
        self.assertEqual(Property.objects.count(), 1)
        self.assertEqual(prop.category, 'house')

    def test_create_property_missing_beds(self):
        """
        Should create Property with default value when beds is missing
        """
        # removes beds from parameters
        del(self.prop_values_one['beds'])
        # asserts there aren't Properties in db
        self.assertEqual(Property.objects.count(), 0)

        # should create Property with default beds value
        prop = Property.objects.create(**self.prop_values_one)
        self.assertEqual(Property.objects.count(), 1)
        self.assertEqual(prop.beds, '1')

    def test_create_property_missing_landlord(self):
        """
        Should raise ValidationError when trying to create Property with
        missing landlord value
        """
        # removes landlord from parameters
        del(self.prop_values_one['landlord'])
        # asserts there aren't Properties in db
        self.assertEqual(Property.objects.count(), 0)

        # should raise validation error when trying to create property
        # with missing landlord value
        expected = {'landlord': [u'This field cannot be null.']}
        with self.assertRaises(ValidationError) as raised:
            Property.objects.create(**self.prop_values_one)
        self.assertEqual(raised.exception.message_dict, expected)
        self.assertEqual(Property.objects.count(), 0)

    def test_property_zip_code_clean(self):
        """Should remove spaces from within zip_code when saving it"""
        self.prop_values_one['zip_code'] = 'NW1   6XE'

        prop = Property.objects.create(**self.prop_values_one)
        self.assertEqual(Property.objects.count(), 1)
        self.assertEqual(prop.zip_code, 'NW16XE')

    def test_property_filtering(self):
        """Should successfully filter property by one of its attributes"""
        Property.objects.create(**self.prop_values_one)
        prop = Property.objects.create(**self.prop_values_two)
        filtered = Property.objects.filter(beds='1')
        self.assertIn(prop, filtered)
        self.assertEqual(len(filtered), 1)

    def test_property_deletion(self):
        """Should successfully delete property from database"""
        self.assertEqual(Property.objects.count(), 0)
        Property.objects.create(**self.prop_values_one)
        prop = Property.objects.create(**self.prop_values_two)
        self.assertEqual(Property.objects.count(), 2)

        Property.objects.filter(beds='1').delete()
        properties = Property.objects.all()
        self.assertEqual(Property.objects.count(), 1)
        self.assertNotIn(prop, properties)

    def test_property_delete_on_landlord_deletion(self):
        """Should successfully delete property on landlord deletion"""
        Property.objects.create(**self.prop_values_one)
        self.assertEqual(Property.objects.count(), 1)
        Landlord.objects.all().delete()
        self.assertEqual(Landlord.objects.count(), 0)
        self.assertEqual(Property.objects.count(), 0)
