# Generated by Django 5.1.3 on 2024-12-10 11:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0006_rename_points_contestparticipation_pionts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestparticipation',
            name='pionts',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]