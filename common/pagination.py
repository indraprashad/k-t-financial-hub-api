from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'per_page'
    max_page_size = 100

    def get_paginated_response(self, data):
        total_pages = self.page.paginator.num_pages
        current_page = self.page.number

        return Response({
            'data': data,
            'meta': {
                'previous': self.get_previous_page_number(),
                'current': current_page,
                'next_page': self.get_next_page_number(),
                'last_page': total_pages,
                'total': self.page.paginator.count,
            }
        })

    def get_previous_page_number(self):
        if self.page.has_previous():
            return self.page.previous_page_number()
        return None

    def get_next_page_number(self):
        if self.page.has_next():
            return self.page.next_page_number()
        return None
