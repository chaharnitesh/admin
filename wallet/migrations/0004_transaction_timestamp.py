# Generated by Django 2.2 on 2020-08-21 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0003_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(max_length=255, null=True),
        ),
    ]
