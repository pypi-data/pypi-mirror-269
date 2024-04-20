# Generated by Django 4.1.7 on 2023-04-22 19:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_subject", "0036_alter_dminitialreview_rx_init_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bloodresultsins",
            name="fasting",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="As reported by patient",
                max_length=15,
                verbose_name="Has the participant fasted?",
            ),
        ),
        migrations.AlterField(
            model_name="dminitialreview",
            name="glucose_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="Glucose date measured"
            ),
        ),
        migrations.AlterField(
            model_name="dminitialreview",
            name="glucose_fasting",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="As reported by patient",
                max_length=15,
                verbose_name="Was glucose measured while fasting?",
            ),
        ),
        migrations.AlterField(
            model_name="dminitialreview",
            name="glucose_fasting_duration_str",
            field=models.CharField(
                blank=True,
                help_text="As reported by patient. Duration of fast. Format is `HHhMMm`. For example 1h23m, 12h7m, etc",
                max_length=8,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc",
                    )
                ],
                verbose_name="How long did they fast (in hours and minutes)?",
            ),
        ),
        migrations.AlterField(
            model_name="dmreview",
            name="glucose_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="Glucose date measured"
            ),
        ),
        migrations.AlterField(
            model_name="dmreview",
            name="glucose_fasting",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="As reported by patient",
                max_length=15,
                verbose_name="Has the participant fasted?",
            ),
        ),
        migrations.AlterField(
            model_name="glucose",
            name="glucose_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="Glucose date measured"
            ),
        ),
        migrations.AlterField(
            model_name="glucose",
            name="glucose_fasting",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="As reported by patient",
                max_length=15,
                verbose_name="Has the participant fasted?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultsins",
            name="fasting",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="As reported by patient",
                max_length=15,
                verbose_name="Has the participant fasted?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldminitialreview",
            name="glucose_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="Glucose date measured"
            ),
        ),
        migrations.AlterField(
            model_name="historicaldminitialreview",
            name="glucose_fasting",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="As reported by patient",
                max_length=15,
                verbose_name="Was glucose measured while fasting?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldminitialreview",
            name="glucose_fasting_duration_str",
            field=models.CharField(
                blank=True,
                help_text="As reported by patient. Duration of fast. Format is `HHhMMm`. For example 1h23m, 12h7m, etc",
                max_length=8,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc",
                    )
                ],
                verbose_name="How long did they fast (in hours and minutes)?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldmreview",
            name="glucose_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="Glucose date measured"
            ),
        ),
        migrations.AlterField(
            model_name="historicaldmreview",
            name="glucose_fasting",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="As reported by patient",
                max_length=15,
                verbose_name="Has the participant fasted?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalglucose",
            name="glucose_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="Glucose date measured"
            ),
        ),
        migrations.AlterField(
            model_name="historicalglucose",
            name="glucose_fasting",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="As reported by patient",
                max_length=15,
                verbose_name="Has the participant fasted?",
            ),
        ),
    ]
