from rest_framework.pagination import PageNumberPagination,CursorPagination

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_query_param='p'
    max_page_size=10
    page_size_query_param='page'
    last_page_strings=['last','end']

class MyCurserPagination(CursorPagination):
    ...
