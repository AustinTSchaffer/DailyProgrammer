# Generated by Django 4.2 on 2023-04-25 12:59

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectMembership',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ProjectMembershipApiKey',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('secret_hash', models.BinaryField(editable=True)),
                ('project_membership_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.projectmembership')),
            ],
        ),
        migrations.AddField(
            model_name='projectmembership',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.projects'),
        ),
        migrations.CreateModel(
            name='DeviceFirmwareUpdateEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('version', models.TextField()),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.device')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceApiKey',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('secret_hash', models.BinaryField(editable=True)),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.device')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='project_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='devices.projects'),
        ),
        migrations.AddConstraint(
            model_name='devicefirmwareupdateevent',
            constraint=models.UniqueConstraint(fields=('device_id', 'timestamp', 'version'), name='unique_device_id_timestamp_version'),
        ),
    ]
