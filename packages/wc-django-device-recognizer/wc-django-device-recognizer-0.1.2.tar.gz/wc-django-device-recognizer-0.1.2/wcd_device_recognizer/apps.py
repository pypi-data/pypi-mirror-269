from django.apps import AppConfig
from django.utils.translation import pgettext_lazy

from .discovery import autodiscover


__all__ = ('DeviceRecognizer',)


class DeviceRecognizer(AppConfig):
    name = 'wcd_device_recognizer'
    verbose_name = pgettext_lazy('wcd_device_recognizer', 'Device recognizer')

    def ready(self):
        autodiscover()
