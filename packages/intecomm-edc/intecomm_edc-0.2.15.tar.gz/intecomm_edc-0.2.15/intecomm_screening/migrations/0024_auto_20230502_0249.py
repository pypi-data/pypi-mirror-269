# Generated by Django 4.1.7 on 2023-05-01 23:49
from django.db import migrations
from django.db.migrations import RunPython
from tqdm import tqdm

from ..identifiers import PatientLogIdentifier


def update_patient_log_identifier(apps, schema_editor):
    patientlog_cls = apps.get_model("intecomm_screening", "patientlog")
    total = patientlog_cls.objects.filter(filing_identifier__isnull=True).count()
    for obj in tqdm(
        patientlog_cls.objects.all(),
        total=total,
    ):
        obj.patient_log_identifier = PatientLogIdentifier(site_id=obj.site_id).identifier
        obj.save_base(update_fields=["patient_log_identifier"])


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_screening", "0023_auto_20230501_2208"),
    ]

    operations = [RunPython(update_patient_log_identifier)]
