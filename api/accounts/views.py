# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, mixins
from django.db import models
from django.shortcuts import get_object_or_404

from accounts.models import Landlord, Tenant
from accounts.serializers import LandlordSerializer, TenantSerializer


class LandlordView(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    This endpoint represents landlords:

    ## Allowed actions:
    *   List all landlords:

        `GET /landlords`

    *   Retrieve one particular landlord:

        `GET /landlords/:id`

    *   Search by landlord name:

        `GET /landlords?search=:query`

    Pagination parameters:

    *   `page`: specifies the page number. If not provided, page 1 is rendered.
    Max value is 1000.

    *   `page_size`: specifies the page size. If not provided, results are
    paginated by 20. Max value is 40. If 'none' is provided, pagination is
    disabled.
    """

    queryset = Landlord.objects.all().order_by('first_name', 'last_name')
    serializer_class = LandlordSerializer

    def filter_queryset(self, queryset):
        queryset = super(LandlordView, self).filter_queryset(queryset)

        # filter by text search
        search = self.request.query_params.get('search')
        if search:
            splitted_search = search.split(' ')
            if len(search) > 1:
                first_name = splitted_search[0]
                last_name = splitted_search[1:]
                queryset = queryset.filter(
                    models.Q(first_name__icontains=first_name) |
                    models.Q(last_name__icontains=last_name))
            else:
                queryset = queryset.filter(
                    models.Q(first_name__icontains=search) |
                    models.Q(last_name__icontains=search))
        return queryset


class TenantView(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """
    This endpoint represents tenants:

    ## Allowed actions:
    *   List all tenants:

        `GET /tenant`

    *   Retrieve one particular tenant:

        `GET /tenants/:id`

    *   Search by tenant name:

        `GET /tenants?search=:query`

    Pagination parameters:

    *   `page`: specifies the page number. If not provided, page 1 is rendered.
    Max value is 1000.

    *   `page_size`: specifies the page size. If not provided, results are
    paginated by 20. Max value is 40. If 'none' is provided, pagination is
    disabled.
    """

    queryset = Tenant.objects.all().order_by('first_name', 'last_name')
    serializer_class = TenantSerializer

    def filter_queryset(self, queryset):
        queryset = super(TenantView, self).filter_queryset(queryset)

        # filter by text search
        search = self.request.query_params.get('search')
        if search:
            splitted_search = search.split(' ')
            if len(search) > 1:
                first_name = splitted_search[0]
                last_name = splitted_search[1:]
                queryset = queryset.filter(
                    models.Q(first_name__icontains=first_name) |
                    models.Q(last_name__icontains=last_name))
            else:
                queryset = queryset.filter(
                    models.Q(first_name__icontains=search) |
                    models.Q(last_name__icontains=search))
        return queryset
