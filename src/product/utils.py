from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):

    page_size = 2
    # page_size_query_param = 'page_size'
    max_page_size = 10000
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        return {
            'status':'success',
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'currentPage': self.page.number
            },
            'count': self.page.paginator.count,
            'total_page': self.page.paginator.num_pages,
            'current_data': len(data),
            'data': data
        }