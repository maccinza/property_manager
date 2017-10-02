# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, mixins
from django.db import models
from rest_framework.permissions import IsAuthenticated

from core.exceptions import Api401
from accounts.models import Landlord, Tenant
from accounts.serializers import (LandlordSerializer,
                                  LandlordModificationSerializer,
                                  TenantSerializer,
                                  TenantModificationSerializer)


class LandlordView(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
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

    permission_classes = (IsAuthenticated,)
    queryset = Landlord.objects.all().order_by('first_name', 'last_name')

    def filter_queryset(self, queryset):
        queryset = super(LandlordView, self).filter_queryset(queryset)
        if self.kwargs.get('pk'):
            return queryset

        # filter by text search
        search = self.request.query_params.get('search')
        if search:
            splitted_search = search.split(' ')
            if len(splitted_search) > 1:
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

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Api401('You do not have the permission to delete '
                         'Landlords information')
        return super(LandlordView, self).destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return LandlordSerializer
        return LandlordModificationSerializer


class TenantView(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
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

    permission_classes = (IsAuthenticated,)
    queryset = Tenant.objects.all().order_by('first_name', 'last_name')

    def filter_queryset(self, queryset):
        queryset = super(TenantView, self).filter_queryset(queryset)

        if self.kwargs.get('pk'):
            return queryset

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

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Api401('You do not have the permission to delete '
                         'Tenants information')
        return super(TenantView, self).destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TenantSerializer
        return TenantModificationSerializer
