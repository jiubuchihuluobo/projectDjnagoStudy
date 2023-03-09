from django.apps import AppConfig
from django.core.signals import request_finished


class JwtauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jwtauth'

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from jwtauth import signals
        # Explicitly connect a signal handler.
        request_finished.connect(
            receiver=signals.my_callback,
            dispatch_uid="3749328fe6734c33821ff7dabe87bf68"
        )

        # 参数dispatch_uid防止重复连接
        request_finished.connect(
            receiver=signals.my_callback,
            dispatch_uid="3749328fe6734c33821ff7dabe87bf68"
        )
