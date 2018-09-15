from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'project.core'

    def ready(self):
        import project.core.signals
