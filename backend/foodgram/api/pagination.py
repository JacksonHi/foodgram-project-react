from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    page_size = 6    # не понял коментарий
# установить "page_size_query_param=limit"?
