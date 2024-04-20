# Generated by Django 5.0 on 2024-01-10 22:15

from django.db import migrations
from django.db.migrations import RunPython


def update_model_name(apps, schema_editor):
    model_cls = apps.get_model("intecomm_consent.subjectconsent")
    model_cls.objects.filter(site_id__lt=200).update(
        model_name="intecomm_consent.subjectconsentug"
    )
    model_cls.objects.filter(site_id__gte=200).update(
        model_name="intecomm_consent.subjectconsent"
    )


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_consent", "0019_historicalsubjectconsent_model_name_and_more"),
    ]

    operations = [RunPython(update_model_name)]
