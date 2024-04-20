# Generated by Django 5.0.4 on 2024-04-12 01:42

import django.core.validators
import edc_model_fields.fields.custom_django_fields
import edc_model_fields.fields.other_charfield
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("intecomm_subject", "0165_careseekinga_care_visit_reason_other_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="careseekinga",
            name="med_collected_location",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                choices=[
                    ("public_pharmacy", "Public pharmacy"),
                    ("private_pharmacy", "Private pharmacy"),
                    ("club", "Club"),
                    ("OTHER", "Other, please specify ..."),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                metadata="FMEDCOLLECTLOC1",
                verbose_name="Where did you collect the medicines from?",
            ),
        ),
        migrations.AddField(
            model_name="careseekinga",
            name="med_collected_location_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                metadata="FMEDCOLLECTLOCOTHER1",
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="historicalcareseekinga",
            name="med_collected_location",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                choices=[
                    ("public_pharmacy", "Public pharmacy"),
                    ("private_pharmacy", "Private pharmacy"),
                    ("club", "Club"),
                    ("OTHER", "Other, please specify ..."),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                metadata="FMEDCOLLECTLOC1",
                verbose_name="Where did you collect the medicines from?",
            ),
        ),
        migrations.AddField(
            model_name="historicalcareseekinga",
            name="med_collected_location_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                metadata="FMEDCOLLECTLOCOTHER1",
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="careseekinga",
            name="care_visit_duration",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                help_text="Invalid format. Please insert a numeric values followed by “h” for hours, and a numeric values followed by “m” for minutes. For example, 1h2m, 0h35m, and so on",
                max_length=5,
                metadata="FFACTIME1",
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Please insert two numeric values followed by “h” for hours, and two numeric values followed by “m” for minute. For example, 01h20m, 00h35m, and so on",
                    )
                ],
                verbose_name="How much time did you spend during your visit today -- from arrival to this place until the end of your visit?",
            ),
        ),
        migrations.AlterField(
            model_name="careseekinga",
            name="med_collected",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                metadata="FMEDCOLL1",
                verbose_name="Did you receive/collect these medicines (whether paid or received for free)?",
            ),
        ),
        migrations.AlterField(
            model_name="careseekinga",
            name="med_cost_dm",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                blank=True,
                help_text="Leave blank if not applicable. In local currency. If medicines were free enter `0`.",
                metadata="FMEDCOSTDM1",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(9999999),
                ],
                verbose_name="How much was spent on Diabetes medicines? ",
            ),
        ),
        migrations.AlterField(
            model_name="careseekinga",
            name="med_cost_hiv",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                blank=True,
                help_text="Leave blank if not applicable. In local currency. If medicines were free enter `0`.",
                metadata="FMEDCOSTHIV1",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(9999999),
                ],
                verbose_name="How much was spent on HIV medicines? ",
            ),
        ),
        migrations.AlterField(
            model_name="careseekinga",
            name="med_cost_htn",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                blank=True,
                help_text="Leave blank if not applicable. In local currency. If medicines were free enter `0`.",
                metadata="FMEDCOSTHTN1",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(9999999),
                ],
                verbose_name="How much was spent on Hypertension medicines? ",
            ),
        ),
        migrations.AlterField(
            model_name="careseekinga",
            name="med_cost_other",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                blank=True,
                help_text="Leave blank if not applicable. In local currency. If medicines were free enter `0`.",
                metadata="FMEDCOSTOTHER1",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(9999999),
                ],
                verbose_name="How much was spent on OTHER medicines? ",
            ),
        ),
        migrations.AlterField(
            model_name="careseekinga",
            name="med_cost_tot",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                blank=True,
                help_text="Leave blank if not applicable. In local currency. If medicines were free enter `0`.",
                metadata="FMEDCOST1",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(9999999),
                ],
                verbose_name="How much was spent on these medicines? ",
            ),
        ),
        migrations.AlterField(
            model_name="careseekinga",
            name="travel_time",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                help_text="Invalid format. Please insert a numeric values followed by “h” for hours, and a numeric values followed by “m” for minutes. For example, 1h2m, 0h35m, and so on",
                max_length=5,
                metadata="FTRATIME1",
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Please insert two numeric values followed by “h” for hours, and two numeric values followed by “m” for minute. For example, 01h20m, 00h35m, and so on",
                    )
                ],
                verbose_name="How long did it take you to reach here?",
            ),
        ),
        migrations.AlterField(
            model_name="careseekinga",
            name="wait_duration",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                help_text="Invalid format. Please insert a numeric values followed by “h” for hours, and a numeric values followed by “m” for minutes. For example, 1h2m, 0h35m, and so on",
                max_length=5,
                metadata="FWAITIME1",
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Please insert two numeric values followed by “h” for hours, and two numeric values followed by “m” for minute. For example, 01h20m, 00h35m, and so on",
                    )
                ],
                verbose_name="How much time did you spend waiting?",
            ),
        ),
        migrations.AlterField(
            model_name="careseekinga",
            name="with_hcw_duration",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                help_text="Invalid format. Please insert a numeric values followed by “h” for hours, and a numeric values followed by “m” for minutes. For example, 1h2m, 0h35m, and so on",
                max_length=5,
                metadata="FWORKTIME1",
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Please insert two numeric values followed by “h” for hours, and two numeric values followed by “m” for minute. For example, 01h20m, 00h35m, and so on",
                    )
                ],
                verbose_name="How much time did you spend with the healthcare worker?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekinga",
            name="care_visit_duration",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                help_text="Invalid format. Please insert a numeric values followed by “h” for hours, and a numeric values followed by “m” for minutes. For example, 1h2m, 0h35m, and so on",
                max_length=5,
                metadata="FFACTIME1",
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Please insert two numeric values followed by “h” for hours, and two numeric values followed by “m” for minute. For example, 01h20m, 00h35m, and so on",
                    )
                ],
                verbose_name="How much time did you spend during your visit today -- from arrival to this place until the end of your visit?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekinga",
            name="med_collected",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                metadata="FMEDCOLL1",
                verbose_name="Did you receive/collect these medicines (whether paid or received for free)?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekinga",
            name="med_cost_dm",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                blank=True,
                help_text="Leave blank if not applicable. In local currency. If medicines were free enter `0`.",
                metadata="FMEDCOSTDM1",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(9999999),
                ],
                verbose_name="How much was spent on Diabetes medicines? ",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekinga",
            name="med_cost_hiv",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                blank=True,
                help_text="Leave blank if not applicable. In local currency. If medicines were free enter `0`.",
                metadata="FMEDCOSTHIV1",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(9999999),
                ],
                verbose_name="How much was spent on HIV medicines? ",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekinga",
            name="med_cost_htn",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                blank=True,
                help_text="Leave blank if not applicable. In local currency. If medicines were free enter `0`.",
                metadata="FMEDCOSTHTN1",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(9999999),
                ],
                verbose_name="How much was spent on Hypertension medicines? ",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekinga",
            name="med_cost_other",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                blank=True,
                help_text="Leave blank if not applicable. In local currency. If medicines were free enter `0`.",
                metadata="FMEDCOSTOTHER1",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(9999999),
                ],
                verbose_name="How much was spent on OTHER medicines? ",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekinga",
            name="med_cost_tot",
            field=edc_model_fields.fields.custom_django_fields.IntegerField2(
                blank=True,
                help_text="Leave blank if not applicable. In local currency. If medicines were free enter `0`.",
                metadata="FMEDCOST1",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(9999999),
                ],
                verbose_name="How much was spent on these medicines? ",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekinga",
            name="travel_time",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                help_text="Invalid format. Please insert a numeric values followed by “h” for hours, and a numeric values followed by “m” for minutes. For example, 1h2m, 0h35m, and so on",
                max_length=5,
                metadata="FTRATIME1",
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Please insert two numeric values followed by “h” for hours, and two numeric values followed by “m” for minute. For example, 01h20m, 00h35m, and so on",
                    )
                ],
                verbose_name="How long did it take you to reach here?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekinga",
            name="wait_duration",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                help_text="Invalid format. Please insert a numeric values followed by “h” for hours, and a numeric values followed by “m” for minutes. For example, 1h2m, 0h35m, and so on",
                max_length=5,
                metadata="FWAITIME1",
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Please insert two numeric values followed by “h” for hours, and two numeric values followed by “m” for minute. For example, 01h20m, 00h35m, and so on",
                    )
                ],
                verbose_name="How much time did you spend waiting?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekinga",
            name="with_hcw_duration",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                help_text="Invalid format. Please insert a numeric values followed by “h” for hours, and a numeric values followed by “m” for minutes. For example, 1h2m, 0h35m, and so on",
                max_length=5,
                metadata="FWORKTIME1",
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Please insert two numeric values followed by “h” for hours, and two numeric values followed by “m” for minute. For example, 01h20m, 00h35m, and so on",
                    )
                ],
                verbose_name="How much time did you spend with the healthcare worker?",
            ),
        ),
    ]
