from rest_framework.authentication import SessionAuthentication


class DisableCsrfSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass
