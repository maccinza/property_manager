from __future__ import unicode_literals

from rest_framework import pagination


class BasePagination(pagination.PageNumberPagination):
    page_size = 20
    max_page_size = 40
    max_page_number = 1000
    page_size_query_param = 'page_size'

    def get_page_size(self, request):
        page_size = request.query_params.get(self.page_size_query_param)
        if page_size and page_size.lower() == 'none':
            return None
        return super(BasePagination, self).get_page_size(request)
