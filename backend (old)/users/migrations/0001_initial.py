# Generated by Django 3.2.8 on 2021-11-11 17:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TimezoneConfiguration',
            fields=[
                ('timezone_id', models.AutoField(primary_key=True, serialize=False)),
                ('timezone', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('usage', models.BooleanField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='timezone_configuration', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RipeUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial_setup_complete', models.BooleanField(default=False)),
                ('ripe_api_token', models.UUIDField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ripe_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
