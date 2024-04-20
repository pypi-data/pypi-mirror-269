# Generated by Django 5.0.4 on 2024-04-12 02:01

import edc_model_fields.fields.custom_django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("intecomm_subject", "0166_careseekinga_med_collected_location_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="careseekinga",
            name="accompany_num",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                blank=True,
                metadata="FACMP1",
                null=True,
                verbose_name="Number of people who accompanied you here today",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekinga",
            name="accompany_num",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                blank=True,
                metadata="FACMP1",
                null=True,
                verbose_name="Number of people who accompanied you here today",
            ),
        ),
    ]
