from rest_framework import serializers
from . import models


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ["id", "name"]


class ProjectApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectApiKey
        fields = ["id", "project_id"]


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Device
        fields = ["id", "project_id"]


class DeviceApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeviceApiKey
        fields = ["id", "device_id"]


class DeviceFirmwareUpdateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeviceFirmwareUpdateEvent
        fields = ["device_id", "timestamp", "version"]
