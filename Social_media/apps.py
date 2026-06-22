from django.apps import AppConfig


class SocialMediaConfig(AppConfig):
    name = 'Social_media'

    def ready(self):
        from.import signals

