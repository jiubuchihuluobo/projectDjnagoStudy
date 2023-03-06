from django.utils.deprecation import MiddlewareMixin


class DisableCsrfMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._dont_enforce_csrf_checks = True
