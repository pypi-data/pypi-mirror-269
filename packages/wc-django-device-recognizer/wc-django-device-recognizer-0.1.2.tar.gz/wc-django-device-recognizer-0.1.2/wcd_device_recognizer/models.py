from typing import Sequence
from uuid import uuid4
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import pgettext_lazy

try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField

from .utils import stringify_version


__all__ = 'App', 'OS', 'Device', 'Interlocutor',


def connect(items: Sequence, check=lambda x: x if x else None) -> str:
    return ' '.join(str(x) for x in items if check(x))


def VersionField(verbose_name=pgettext_lazy('wcd_device_recognizer', 'Version')):
    return ArrayField(
        models.IntegerField(), verbose_name=verbose_name,
        blank=True, default=list,
    )


class UUIDable(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(
        verbose_name=pgettext_lazy('wcd_device_recognizer', 'ID'),
        primary_key=True, default=uuid4,
    )

    created_at = models.DateTimeField(
        verbose_name=pgettext_lazy('wcd_device_recognizer', 'Created at'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=pgettext_lazy('wcd_device_recognizer', 'Updated at'),
        auto_now=True
    )


class Versionable(UUIDable):
    class Meta:
        abstract = True

    version = VersionField()

    @property
    def version_string(self):
        return stringify_version(self.version)


class Familia(models.Model):
    class Meta:
        abstract = True

    family = models.CharField(
        pgettext_lazy('wcd_device_recognizer', 'Family'),
        max_length=1024, db_index=True, blank=True,
    )


class App(Versionable, Familia):
    class Meta:
        verbose_name = pgettext_lazy('wcd_device_recognizer', 'App')
        verbose_name_plural = pgettext_lazy('wcd_device_recognizer', 'Apps')

    def __str__(self):
        return connect((self.family, self.version_string))


class OS(Versionable, Familia):
    class Meta:
        verbose_name = pgettext_lazy('wcd_device_recognizer', 'OS')
        verbose_name_plural = pgettext_lazy('wcd_device_recognizer', 'OSs')

    arch = models.CharField(
        pgettext_lazy('wcd_device_recognizer', 'Architecture'),
        max_length=24, db_index=True, blank=True,
    )

    def __str__(self):
        return connect((self.family, self.version_string, self.arch))


class Device(UUIDable, Familia):
    class Meta:
        verbose_name = pgettext_lazy('wcd_device_recognizer', 'Device')
        verbose_name_plural = pgettext_lazy('wcd_device_recognizer', 'Devices')

    brand = models.CharField(
        pgettext_lazy('wcd_device_recognizer', 'Brand'),
        max_length=1024, db_index=True, blank=True,
    )
    model = models.CharField(
        pgettext_lazy('wcd_device_recognizer', 'Model'),
        max_length=1024, db_index=True, blank=True,
    )
    bitness = models.CharField(
        pgettext_lazy('wcd_device_recognizer', 'Bitness'),
        max_length=24, db_index=True, blank=True,
    )
    memory = models.DecimalField(
        pgettext_lazy('wcd_device_recognizer', 'Memory'),
        decimal_places=4, max_digits=28, null=True, blank=True,
    )
    dpr = models.DecimalField(
        pgettext_lazy('wcd_device_recognizer', 'DPR'),
        decimal_places=6, max_digits=28, default=1,
    )
    viewport_width = models.IntegerField(
        pgettext_lazy('wcd_device_recognizer', 'Viewport width'),
        null=True, blank=True,
    )

    def __str__(self):
        return connect((self.brand, self.model)) or self.family


class InterlocutorQuerySet(models.QuerySet):
    def with_relateds(self):
        return self.select_related('os', 'app', 'device')


class Interlocutor(UUIDable):
    # type: models.Manager[InterlocutorQuerySet]
    objects = InterlocutorQuerySet.as_manager()

    class Meta:
        verbose_name = pgettext_lazy('wcd_device_recognizer', 'Interlocutor')
        verbose_name_plural = pgettext_lazy('wcd_device_recognizer', 'Interlocutors')

    os = models.ForeignKey(
        OS, on_delete=models.SET_NULL, related_name='interlocutors',
        verbose_name=pgettext_lazy('wcd_device_recognizer', 'OS'),
        null=True, blank=True,
    )
    app = models.ForeignKey(
        App, on_delete=models.SET_NULL, related_name='interlocutors',
        verbose_name=pgettext_lazy('wcd_device_recognizer', 'App'),
        null=True, blank=True,
    )
    device = models.ForeignKey(
        Device, on_delete=models.SET_NULL, related_name='interlocutors',
        verbose_name=pgettext_lazy('wcd_device_recognizer', 'Device'),
        null=True, blank=True,
    )

    outer_id = models.TextField(
        verbose_name=pgettext_lazy('wcd_device_recognizer', 'Device/App identifier'),
        blank=True,
    )
    user_agent = models.TextField(
        verbose_name=pgettext_lazy('wcd_device_recognizer', 'User Agent string'),
        blank=True,
    )
    client_hints = JSONField(
        verbose_name=pgettext_lazy('wcd_device_recognizer', 'Client hints'),
        default=dict,
    )

    def __str__(self):
        return f'#{self.id}'


class InterlocutorNetwork(UUIDable):
    class Meta:
        verbose_name = pgettext_lazy('wcd_device_recognizer', 'Interlocutor network info')
        verbose_name_plural = pgettext_lazy('wcd_device_recognizer', 'Interlocutor network infos')

    interlocutor = models.ForeignKey(
        Interlocutor, on_delete=models.CASCADE, related_name='network_connections',
        verbose_name=pgettext_lazy('wcd_device_recognizer', 'Interlocutor'),
    )
    ip = models.GenericIPAddressField(
        verbose_name=pgettext_lazy('wcd_device_recognizer', 'IP Address'),
        null=False, blank=False,
    )

    def __str__(self):
        return f'Interlocutor #{self.interlocutor_id} connection from {self.ip}'
