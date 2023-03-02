from django.apps import AppConfig


class CustomauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customauth'

    def ready(self):
        import customauth.signal
