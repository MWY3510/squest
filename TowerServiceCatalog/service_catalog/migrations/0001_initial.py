# Generated by Django 3.1.7 on 2021-03-08 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TowerServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=200)),
                ('token', models.CharField(max_length=200)),
                ('secure', models.BooleanField(default=True)),
                ('ssl_verify', models.BooleanField(default=False)),
            ],
        ),
    ]
