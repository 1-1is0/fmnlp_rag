# Generated by Django 5.0.1 on 2024-02-01 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentmodel',
            name='proccsed',
            field=models.BooleanField(default=False),
        ),
    ]