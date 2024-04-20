# Generated by Django 4.2.9 on 2024-02-01 14:14

import django.contrib.sites.managers
from django.db import migrations

import intecomm_consent.models.subject_consent


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_consent", "0022_subjectconsenttz_historicalsubjectconsenttz"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="subjectconsent",
            managers=[
                ("objects", intecomm_consent.models.subject_consent.ConsentObjectsManager()),
                ("on_site", django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
    ]
