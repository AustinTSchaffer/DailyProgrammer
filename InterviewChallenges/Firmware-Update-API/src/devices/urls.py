from django.urls import path

from . import views

urlpatterns = [
    path(
        'devices/<uuid:id>/firmware_version',
        views.DeviceFirmwareVersionsView.as_view(),
        name='firmware_versions'
    ),
    path('seed', views.seed_database, name='seed')
]
