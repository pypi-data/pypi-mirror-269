# Generated by Django 4.2.5 on 2023-10-05 23:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_subject", "0121_auto_20231006_0238"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalnextappointment",
            name="info_source_old",
        ),
        migrations.RemoveField(
            model_name="nextappointment",
            name="info_source_old",
        ),
    ]
