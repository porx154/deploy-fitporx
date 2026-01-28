from django.apps import AppConfig


class FitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.fit'

    def ready(self):
        import apps.fit.signals