from rest_framework.authentication import SessionAuthentication, TokenAuthentication


class DisableCsrfSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass


class BearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'
