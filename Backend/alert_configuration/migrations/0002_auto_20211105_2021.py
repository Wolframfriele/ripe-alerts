# Generated by Django 3.2.8 on 2021-11-05 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('alert_configuration', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alertconfiguration',
            old_name='measurement_id',
            new_name='measurement',
        ),
        migrations.AddField(
            model_name='alertconfiguration',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='users.ripeuser'),
            preserve_default=False,
        ),
    ]
