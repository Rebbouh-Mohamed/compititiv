# Generated by Django 5.1.3 on 2024-12-07 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0004_submitcase_testcase'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='is_submitted',
            field=models.BooleanField(default=False),
        ),
    ]