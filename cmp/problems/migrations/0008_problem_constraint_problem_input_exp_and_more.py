# Generated by Django 5.1.3 on 2024-12-18 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0007_problem_input_description_problem_output_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='constraint',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='problem',
            name='input_exp',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='problem',
            name='output_exp',
            field=models.TextField(default=''),
        ),
    ]
