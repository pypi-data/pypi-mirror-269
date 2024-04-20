# Generated by Django 4.2.1 on 2023-05-23 23:20

from django.db import migrations
import edc_model_fields.fields.other_charfield


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_subject", "0044_healtheconomicshouseholdhead_hoh_education_other_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="healtheconomicshouseholdhead",
            name="hoh_marital_status_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If OTHER marital status, specify ...",
            ),
        ),
        migrations.AddField(
            model_name="historicalhealtheconomicshouseholdhead",
            name="hoh_marital_status_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If OTHER marital status, specify ...",
            ),
        ),
    ]
