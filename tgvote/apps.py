from django.apps import AppConfig


class TgvoteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tgvote'

    def ready(self):
        import tgvote.signals