# Generated by Django 4.2.3 on 2023-07-25 21:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        # ("intecomm_facility", "0002_alter_healthfacility_device_created_and_more"),
        ("intecomm_subject", "0064_historicalnextappointment_health_facility_old_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalnextappointment",
            name="old_health_facility",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="nextappointment",
            name="old_health_facility",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
