# Generated by Django 3.2.8 on 2021-11-06 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Target',
            fields=[
                ('target_id', models.IntegerField(primary_key=True, serialize=False)),
                ('target_type', models.CharField(choices=[('Extern', 'Extern'), ('Probe', 'Probe')], default='Probe', max_length=10)),
                ('probe_id', models.IntegerField(unique=True)),
                ('prefix_v4', models.CharField(blank=True, default='', max_length=128)),
                ('prefix_v6', models.CharField(blank=True, default='', max_length=128)),
                ('ip_v4', models.CharField(blank=True, default='', max_length=128)),
                ('ip_v6', models.CharField(blank=True, default='', max_length=128)),
                ('asn_v4', models.CharField(blank=True, default='', max_length=128)),
                ('asn_v6', models.CharField(blank=True, default='', max_length=128)),
                ('host', models.CharField(blank=True, default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('measurement_id', models.IntegerField(primary_key=True, serialize=False)),
                ('measurement_type', models.CharField(choices=[('Ping', 'Ping'), ('Traceroute', 'Traceroute'), ('Dns', 'Dns'), ('Sslcert', 'Sslcert'), ('Http', 'Http'), ('Ntp', 'Ntp')], max_length=10)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ripe_atlas.target')),
            ],
        ),
    ]
