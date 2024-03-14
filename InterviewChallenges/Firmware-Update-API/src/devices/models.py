from django.db import models
import uuid


class Project(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.TextField()


class ProjectApiKey(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    project_id = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=False,
    )

    secret_hash = models.BinaryField(
        editable=True,
        null=False,
    )


class Device(models.Model):
    """
    Core model for recording information about a device.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    project_id = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
    )


class DeviceApiKey(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    device_id = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        null=False,
    )

    secret_hash = models.BinaryField(
        editable=True,
        null=False,
    )


class DeviceFirmwareUpdateEvent(models.Model):
    """
    This is the model that records device firmware update events.
    The event consists of a timestamp and a version.
    """

    device_id = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        null=False,
    )

    timestamp = models.DateTimeField(
        null=False,
    )

    version = models.TextField(
        null=False,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['device_id', 'timestamp', 'version'], name='unique_device_id_timestamp_version'
            )
        ]

        indexes = [
            models.Index(
                fields=['device_id'], name='device_id_idx'
            )
        ]
