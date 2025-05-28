# from django.apps import AppConfig


# class TextappConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'textapp'

from django.apps import AppConfig

class TextappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'textapp'

    def ready(self):
        import textapp.signals  # This imports signals.py
