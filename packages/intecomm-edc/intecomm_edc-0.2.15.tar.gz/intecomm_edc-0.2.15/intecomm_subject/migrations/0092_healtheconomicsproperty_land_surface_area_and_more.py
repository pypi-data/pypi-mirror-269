# Generated by Django 4.2.3 on 2023-08-07 22:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_subject", "0091_healtheconomicsassets_solar_panels_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="healtheconomicsproperty",
            name="land_surface_area",
            field=models.IntegerField(
                blank=True,
                help_text="Surface area in acres or m2. (Note 1 hector ~= 2.5 acres)",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(999999999),
                ],
                verbose_name="Surface area",
            ),
        ),
        migrations.AddField(
            model_name="healtheconomicsproperty",
            name="land_surface_area_units",
            field=models.CharField(
                blank=True,
                choices=[
                    ("hectares", "hectares"),
                    ("acres", "acres"),
                    ("sq_meters", "sq. meters"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=15,
                null=True,
                verbose_name="Surface area (units)",
            ),
        ),
        migrations.AddField(
            model_name="historicalhealtheconomicsproperty",
            name="land_surface_area",
            field=models.IntegerField(
                blank=True,
                help_text="Surface area in acres or m2. (Note 1 hector ~= 2.5 acres)",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(999999999),
                ],
                verbose_name="Surface area",
            ),
        ),
        migrations.AddField(
            model_name="historicalhealtheconomicsproperty",
            name="land_surface_area_units",
            field=models.CharField(
                blank=True,
                choices=[
                    ("hectares", "hectares"),
                    ("acres", "acres"),
                    ("sq_meters", "sq. meters"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=15,
                null=True,
                verbose_name="Surface area (units)",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomicsproperty",
            name="land_additional_known",
            field=models.CharField(
                default="QUESTION_RETIRED",
                help_text="Use cash equivalent in local currency",
                max_length=25,
                verbose_name="Do you know about how much is this worth in total?",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomicsproperty",
            name="land_owner",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("dont_know", "Do not know"),
                    ("DWTA", "Don't want to answer"),
                ],
                max_length=25,
                verbose_name="Do you own any land.",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomicsproperty",
            name="land_value",
            field=models.IntegerField(
                blank=True,
                help_text="Use cash equivalent in local currency",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(999999999),
                ],
                verbose_name="About how much this is worth in total?",
            ),
        ),
        migrations.AlterField(
            model_name="healtheconomicsproperty",
            name="land_value_known",
            field=models.CharField(
                default="QUESTION_RETIRED",
                help_text="Use cash equivalent in local currency",
                max_length=25,
                verbose_name="Do you know about how much this is worth in total?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicsproperty",
            name="land_additional_known",
            field=models.CharField(
                default="QUESTION_RETIRED",
                help_text="Use cash equivalent in local currency",
                max_length=25,
                verbose_name="Do you know about how much is this worth in total?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicsproperty",
            name="land_owner",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("dont_know", "Do not know"),
                    ("DWTA", "Don't want to answer"),
                ],
                max_length=25,
                verbose_name="Do you own any land.",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicsproperty",
            name="land_value",
            field=models.IntegerField(
                blank=True,
                help_text="Use cash equivalent in local currency",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(999999999),
                ],
                verbose_name="About how much this is worth in total?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhealtheconomicsproperty",
            name="land_value_known",
            field=models.CharField(
                default="QUESTION_RETIRED",
                help_text="Use cash equivalent in local currency",
                max_length=25,
                verbose_name="Do you know about how much this is worth in total?",
            ),
        ),
    ]
