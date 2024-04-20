# Generated by Django 4.2.1 on 2023-07-05 02:16

import django.db.models.deletion
import edc_screening.model_mixins.screening_model_mixin
import edc_sites.models
from django.db import migrations, models

import intecomm_screening.model_mixins.patient_call_model_mixin
import intecomm_screening.models.health_talk_log
import intecomm_screening.models.patient_log


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_screening", "0041_auto_20230702_1548"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="healthfacility",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Health Facility",
                "verbose_name_plural": "Health Facilities",
            },
        ),
        migrations.AlterModelOptions(
            name="healthtalklog",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Health talk log",
                "verbose_name_plural": "Health talk logs",
            },
        ),
        migrations.AlterModelOptions(
            name="idenfifierformat",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Idenfifier format",
                "verbose_name_plural": "Idenfifier formats",
            },
        ),
        migrations.AlterModelOptions(
            name="patientlog",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Patient Log",
                "verbose_name_plural": "Patient Log",
            },
        ),
        migrations.AlterModelOptions(
            name="patientlogreportprinthistory",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
            },
        ),
        migrations.AlterModelManagers(
            name="healthtalklog",
            managers=[
                ("objects", intecomm_screening.models.health_talk_log.Manager()),
                ("on_site", edc_sites.models.CurrentSiteManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="patientcall",
            managers=[
                (
                    "objects",
                    intecomm_screening.model_mixins.patient_call_model_mixin.Manager(),
                ),
                ("on_site", edc_sites.models.CurrentSiteManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="patientlog",
            managers=[
                ("objects", intecomm_screening.models.patient_log.PatientLogManager()),
                ("on_site", edc_sites.models.CurrentSiteManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="subjectscreening",
            managers=[
                (
                    "objects",
                    edc_screening.model_mixins.screening_model_mixin.ScreeningManager(),
                ),
                ("on_site", edc_sites.models.CurrentSiteManager()),
            ],
        ),
    ]
