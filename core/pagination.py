from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class PageCountPagination(PageNumberPagination):
    """
    Pagination style that returns the page, page count and the results.
    """

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('page', self.page.number),
            ('page_count', self.page.paginator.num_pages),
            ('results', data)
        ]))
