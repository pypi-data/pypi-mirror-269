# Generated by Django 4.2.10 on 2024-02-22 07:18

from django.db import migrations
import edc_model_fields.fields.custom_django_fields


class Migration(migrations.Migration):

    dependencies = [
        (
            "intecomm_subject",
            "0146_rename_seek_inpatient_visits_careseekingb_inpatient_days_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="careseekinga",
            name="accompany_num",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                metadata="FACMP1",
                verbose_name="Number of people who accompanied you here today",
            ),
        ),
        migrations.AlterField(
            model_name="careseekingb",
            name="accompany_num",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                metadata="FOUTACMPNUM1",
                verbose_name="Number of people who accompanied you here today",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekinga",
            name="accompany_num",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                metadata="FACMP1",
                verbose_name="Number of people who accompanied you here today",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekingb",
            name="accompany_num",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                metadata="FOUTACMPNUM1",
                verbose_name="Number of people who accompanied you here today",
            ),
        ),
    ]
