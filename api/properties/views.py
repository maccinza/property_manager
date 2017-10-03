# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from copy import deepcopy

from django.core.exceptions import ValidationError
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from core.exceptions import Api400, Api401, Api404
from accounts.models import Landlord
from properties.models import Property
from properties.validators import is_category_valid, is_number_of_beds_valid
from properties.serializers import (PropertySerializer,
                                    PropertyModificationsSerializer)


class PropertyView(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    This endpoint represents properties:

    ## Allowed actions:
    *   List all properties:

        `GET /properties`

    *   Retrieve one particular property:

        `GET /properties/:id`

    *  Create Property:

        `POST /properties`

        Sample payload:

        ```
        {
            'street': 'Riverdale Avenue',
            'number': '78',
            'city': 'South Yorkshire',
            'zip_code': 'SY79XEW',
            'description': 'Incredible property with nice location',
            'beds': '2',
            'category': 'house',
            'landlord': 'aryh149jfl0pol1r'
        }
        ``` 

    *  Update Property:

        `PUT /properties/:id`

        Sample payload:

        ```
        {
            'street': 'Riverdale Avenue',
            'number': '78',
            'city': 'South Yorkshire',
            'zip_code': 'SY79XEW',
            'description': 'Incredible property with nice location',
            'beds': '2',
            'category': 'house',
            'landlord': 'aryh149jfl0pol1r'
        }
        ```

    * Partially update Property:

        `PATCH /properties/:id`

        Sample payload:

        ```
        {
            'street': 'Riverdale Avenue',
            'number': '78'
        }
        ```

    Available filters:

    *   `landlord_id`: Filters properties by landlord

        `GET /properties?landlord_id=landlord_id`

    *   `city`: Filters properties by city

        `GET /properties?city=city_name`

    *   `zipcode`: Filters properties by zip_code

        `GET /properties?zipcode=zipcode`

    *   `street`: Filters properties by street

        `GET /properties?street=street_name`

    *   `category`: Filters properties by category

        `GET /properties?category=category_name`

        Valid values for category_name are house, apartment, flat, other

    *   `beds`: Filters properties by number of bedrooms

        `GET /properties?beds=beds_number`

        Valid values for beds_number are 1, 2, 3, 4+

    Pagination parameters:

    *   `page`: specifies the page number. If not provided, page 1 is rendered.
    Max value is 1000.

    *   `page_size`: specifies the page size. If not provided, results are
    paginated by 20. Max value is 40. If 'none' is provided, pagination is
    disabled.
    """

    permission_classes = (IsAuthenticated,)
    queryset = Property.objects.all().order_by(
        'city', 'zip_code', 'street')

    def filter_queryset(self, queryset):
        queryset = super(PropertyView, self).filter_queryset(queryset)
        if self.kwargs.get('pk'):
            return queryset

        # filter by landlord
        landlord = self.request.query_params.get('landlord_id')
        if landlord:
            queryset = queryset.filter(landlord=landlord)

        # filter by city
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)

        # filter by zipcode
        zipcode = self.request.query_params.get('zipcode')
        if zipcode:
            zipcode = zipcode.replace(' ', '')
            queryset = queryset.filter(zip_code=zipcode)

        # fiter by street
        street = self.request.query_params.get('street')
        if street:
            queryset = queryset.filter(street__icontains=street)

        # filter by category
        category = self.request.query_params.get('category')
        if category:
            category = category.lower()
            if is_category_valid(category):
                queryset = queryset.filter(category=category)
            else:
                raise Api400(
                    'Invalid category "{}" for property'.format(category))

        # filter by beds
        beds = self.request.query_params.get('beds')
        if beds:
            if is_number_of_beds_valid(beds):
                queryset = queryset.filter(beds=beds)
            else:
                raise Api400(
                    'Invalid number of beds "{}" for property'.format(beds))
        return queryset

    def create(self, request, *args, **kwargs):
        landlord_id = request.data.get('landlord', None)
        if landlord_id:
            try:
                landlord = Landlord.objects.get(id=landlord_id)
            except Exception:
                raise Api404('Landlord with id "{}" does '
                             'not exist'.format(landlord_id))
        else:
            raise Api400('Missing landlord parameter contaning landlord id')

        data = request.data.dict()
        data['landlord'] = landlord
        try:
            aproperty = Property.objects.create(**data)
        except ValidationError as e:
            raise Api400(e.message_dict)
        context = self.get_serializer_context()
        serializer = PropertyModificationsSerializer(
            aproperty, context=context)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Api401('You do not have the permission to delete '
                         'Properties information')
        return super(PropertyView, self).destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return PropertySerializer
        return PropertyModificationsSerializer
