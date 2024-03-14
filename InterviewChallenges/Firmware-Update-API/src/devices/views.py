import secrets
import string
import base64
import datetime
import json

import bcrypt
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from . import models, serializers

SECRET_CHARACTERS = string.ascii_letters + string.digits
SECRET_LENGTH = 20


def seed_database(request):
    # Create a project
    project = models.Project(name="Test Project")
    project.save()

    # Create a project-level API key.

    project_api_key_secret = "".join(
        (secrets.choice(SECRET_CHARACTERS) for _ in range(SECRET_LENGTH))
    )
    project_api_key = models.ProjectApiKey(
        project_id=project,
        secret_hash=bcrypt.hashpw(
            project_api_key_secret.encode("utf8"), bcrypt.gensalt()
        ),
    )
    project_api_key.save()

    # Create a device
    device = models.Device(project_id=project)
    device.save()

    device_api_key_secret = "".join(
        (secrets.choice(SECRET_CHARACTERS) for _ in range(SECRET_LENGTH))
    )
    device_api_key = models.DeviceApiKey(
        device_id=device,
        secret_hash=bcrypt.hashpw(
            device_api_key_secret.encode("utf8"), bcrypt.gensalt()
        ),
    )
    device_api_key.save()

    # Serialize and send
    project_serializer = serializers.ProjectSerializer(project)
    project_api_key_serializer = serializers.ProjectApiKeySerializer(project_api_key)
    device_serializer = serializers.DeviceSerializer(device)
    device_api_key_serializer = serializers.DeviceApiKeySerializer(device_api_key)

    return JsonResponse(
        {
            "project": project_serializer.data,
            "project_api_key": project_api_key_serializer.data,
            "project_api_key_secret": project_api_key_secret,
            "device": device_serializer.data,
            "device_api_key": device_api_key_serializer.data,
            "device_api_key_secret": device_api_key_secret,
        },
        status=201,
    )


def parse_basic_auth_header(request) -> tuple[str, str]:
    auth_header = request.headers.get("Authorization", None)
    if not auth_header:
        return None, None

    auth_scheme, *auth_params = auth_header.split(" ")
    if auth_scheme.lower() != "basic":
        return None, None

    if len(auth_params) != 1:
        return None, None

    username, password = base64.b64decode(auth_params[0]).decode("utf-8").split(":")
    return username, password


@method_decorator(csrf_exempt, name="dispatch")
class DeviceFirmwareVersionsView(View):
    def post(self, request, id=None, *args, **kwargs):
        """
        Allow a single device to upload their current firmware version.
        """

        # Validate Device's API Key

        api_key_id, api_key_secret = parse_basic_auth_header(request)
        if not api_key_id or not api_key_secret:
            return HttpResponse(status=401)

        device_api_key = models.DeviceApiKey.objects.filter(id=api_key_id).first()
        if not device_api_key:
            return HttpResponse(status=401)

        valid_api_key = bcrypt.checkpw(
            api_key_secret.encode("utf-8"), device_api_key.secret_hash.tobytes()
        )
        if not valid_api_key:
            return HttpResponse(status=401)

        # Check Authorization

        if id != device_api_key.device_id.id:
            return HttpResponse(status=403)

        # Check for request validity.

        event = json.loads(request.body.decode())
        if "version" not in event:
            return JsonResponse(
                {"validation": "missing 'version' property."}, status=400
            )

        # TODO: Validate semantic versioning?

        firmware_version_update_event = models.DeviceFirmwareUpdateEvent(
            device_id=device_api_key.device_id,
            version=event["version"],
            timestamp=datetime.datetime.now(tz=timezone.utc),
        )

        firmware_version_update_event.save()

        response_ser = serializers.DeviceFirmwareUpdateEventSerializer(
            firmware_version_update_event
        )

        return JsonResponse(response_ser.data, status=201)

    def get(self, request, id=None, *args, **kwargs):
        """
        Allow a project member to retrieve all of the virmware versions for
        a single device.
        """

        # Validate Project API Key

        api_key_id, api_key_secret = parse_basic_auth_header(request)
        if not api_key_id or not api_key_secret:
            return HttpResponse(status=401)

        project_api_key = models.ProjectApiKey.objects.filter(id=api_key_id).first()
        if not project_api_key:
            return HttpResponse(status=401)

        valid_api_key = bcrypt.checkpw(
            api_key_secret.encode("utf-8"), project_api_key.secret_hash.tobytes()
        )
        if not valid_api_key:
            return HttpResponse(status=401)

        # Check Authorization

        device = models.Device.objects.filter(id=id).first()
        if not device or project_api_key.project_id != device.project_id:
            return HttpResponse(status=404)

        # Retrieve records.

        firmware_version_update_events = models.DeviceFirmwareUpdateEvent.objects.filter(device_id=device)

        response_ser = serializers.DeviceFirmwareUpdateEventSerializer(
            firmware_version_update_events,
            many=True
        )

        return JsonResponse(response_ser.data, safe=False)
