from django.apps import AppConfig


class CryptoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crypto_app'
    verbose_name = 'CryptoHub'

    def ready(self):
        pass
