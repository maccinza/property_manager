from __future__ import unicode_literals

from rest_framework import pagination


class BasePagination(pagination.PageNumberPagination):
    page_size = 20
    max_page_size = 40
    max_page_number = 1000
    page_size_query_param = 'page_size'
