# Generated by Django 5.1.3 on 2024-12-10 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codingspace', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultcode',
            name='language',
            field=models.CharField(choices=[('C', 'C'), ('CPP', 'C++'), ('CS', 'C#'), ('JAVA', 'Java'), ('JS', 'JavaScript'), ('PY', 'Python'), ('GO', 'Go')], max_length=10),
        ),
    ]