# Generated by Django 4.2.1 on 2023-06-30 22:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_lists", "0006_consentrefusalreasons_screeningrefusalreasons_and_more"),
        (
            "intecomm_screening",
            "0036_alter_historicalpatientlog_screening_identifier_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="consentrefusal",
            name="screening_identifier",
            field=models.CharField(max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name="consentrefusal",
            name="subject_screening",
            field=models.OneToOneField(
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="intecomm_screening.subjectscreening",
            ),
        ),
        migrations.AlterField(
            model_name="historicalconsentrefusal",
            name="screening_identifier",
            field=models.CharField(db_index=True, max_length=36),
        ),
        migrations.AlterField(
            model_name="historicalpatientlog",
            name="willing_to_screen",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("tbd", "To be determined")],
                default="tbd",
                max_length=15,
                verbose_name="Has the patient agreed to be screened for the INTECOMM study",
            ),
        ),
        migrations.AlterField(
            model_name="patientlog",
            name="screening_refusal_reason",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="intecomm_lists.screeningrefusalreasons",
                verbose_name="Reason subject unwilling to screen",
            ),
        ),
        migrations.AlterField(
            model_name="patientlog",
            name="willing_to_screen",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("tbd", "To be determined")],
                default="tbd",
                max_length=15,
                verbose_name="Has the patient agreed to be screened for the INTECOMM study",
            ),
        ),
    ]
