# Generated by Django 5.1.3 on 2024-12-05 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0004_submission_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='language',
            field=models.TextField(max_length=10),
        ),
    ]
