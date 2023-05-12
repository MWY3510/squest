# Generated by Django 3.2.13 on 2022-10-04 16:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service_catalog', '0011_auto_20221003_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='accepted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accepted_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='request',
            name='processed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='processed_requests', to=settings.AUTH_USER_MODEL),
        ),
    ]