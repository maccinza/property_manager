# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from core.exceptions import Api400, Api401, Api404
from accounts.models import Tenant
from properties.models import Property
from contracts.serializers import (ContractSerializer,
                                   ContractModificationsSerializer)
from contracts.models import Contract


class ContractView(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    This endpoint represents contracts:

    ## Allowed actions:
    *   List all Contracts:

        `GET /contracts`

    *   Retrieve one particular Contract:

        `GET /contracts/:id`

    *  Create Contract:

        `POST /contracts`

        Sample payload:

        ```
        {
            'property': 'ui981khf60pclax2',
            'tenant': 'aryh149jfl0pol1r',
            'start_date': '2017-09-10',
            'end_date': '2018-09-10'
        }
        ```

    *  Update Contract:

        `PUT /contracts/:id`

        Sample payload:

        ```
        {
            'property': 'ui981khf60pclax2',
            'tenant': 'aryh149jfl0pol1r',
            'start_date': '2017-12-10',
            'end_date': '2018-12-10'
        }
        ```

    * Partially update Contract:

        `PATCH /contracts/:id`

        Sample payload:

        ```
        {
            'start_date': '2017-12-10',
        }
        ```

    Available filters:

    *   `tenant_id`: Filters contracts by tenant

        `GET /contracts?tenant_id=tenant_id`

    *   `property_id`: Filters contracts by property

        `GET /contracts?property_id=property_id`

    *   `start_date`: Filters contracts with start date greater than the given

        `GET /contracts?start_date=given_date`

    *   `end_date`: Filters contracts with end date lower than the given

        `GET /contracts?end_date=given_date`

    Pagination parameters:

    *   `page`: specifies the page number. If not provided, page 1 is rendered.
    Max value is 1000.

    *   `page_size`: specifies the page size. If not provided, results are
    paginated by 20. Max value is 40. If 'none' is provided, pagination is
    disabled.
    """

    permission_classes = (IsAuthenticated,)
    queryset = Contract.objects.all().order_by('-created')

    def filter_queryset(self, queryset):
        queryset = super(ContractView, self).filter_queryset(queryset)
        if self.kwargs.get('pk'):
            return queryset

        # filter by tenant
        tenant = self.request.query_params.get('tenant_id')
        if tenant:
            queryset = queryset.filter(tenant=tenant)

        # filter by property
        property_id = self.request.query_params.get('property_id')
        if property_id:
            queryset = queryset.filter(property=property_id)

        # filter by start_date
        start_date = self.request.query_params.get('start_date')
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)

        # fiter by end_date
        end_date = self.request.query_params.get('end_date')
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)

        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data.dict()

        property_id = data.get('property', None)
        if property_id:
            try:
                dproperty = Property.objects.get(id=property_id)
            except Exception:
                raise Api404('Property with id "{}" does '
                             'not exist'.format(property_id))
        else:
            raise Api400('Missing property parameter contaning property id')
        data['property'] = dproperty

        tenant_id = data.get('tenant', None)
        if tenant_id:
            try:
                tenant = Tenant.objects.get(id=tenant_id)
            except Exception:
                raise Api404('Tenant with id "{}" does '
                             'not exist'.format(tenant_id))
        else:
            raise Api400('Missing tenant parameter contaning tenant id')
        data['tenant'] = tenant

        try:
            contract = Contract.objects.create(**data)
        except ValidationError as e:
            raise Api400(e.message_dict)

        context = self.get_serializer_context()
        serializer = ContractModificationsSerializer(contract, context=context)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Api401('You do not have the permission to delete '
                         'Contracts information')
        return super(ContractView, self).destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ContractSerializer
        return ContractModificationsSerializer
