from rest_framework.pagination import PageNumberPagination, CursorPagination


class MyPageNumberPagination(PageNumberPagination):
    """
    A simple page number based style that supports page numbers as
    query parameters. For example:

    http://api.example.org/accounts/?page=4
    http://api.example.org/accounts/?page=4&page_size=100
    """
    # Client can control the page using this query parameter.
    page_query_param = 'page'

    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = "page_size"

    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.
    max_page_size = 20


class MyCursorPagination(CursorPagination):
    cursor_query_param = 'cursor'
    ordering = '-date_joined'

    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = "page_size"

    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.
    max_page_size = 20

    # The offset in the cursor is used in situations where we have a
    # nearly-unique index. (Eg millisecond precision creation timestamps)
    # We guard against malicious users attempting to cause expensive database
    # queries, by having a hard cap on the maximum possible size of the offset.
    offset_cutoff = 1000
