# Generated by Django 4.1.2 on 2023-01-27 01:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_subject", "0009_remove_historicalvitals_bp_measured_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalvitals",
            name="weight_is_estmated",
        ),
        migrations.RemoveField(
            model_name="vitals",
            name="weight_is_estmated",
        ),
        migrations.AddField(
            model_name="historicalvitals",
            name="comments",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="historicalvitals",
            name="weight_determination",
            field=models.CharField(
                choices=[
                    ("measured", "Measured"),
                    ("estimated", "Estimated"),
                    ("N/A", "Not recorded / Not applicable"),
                ],
                default="measured",
                max_length=15,
                verbose_name="Is weight estimated or measured?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="vitals",
            name="comments",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="vitals",
            name="weight_determination",
            field=models.CharField(
                choices=[
                    ("measured", "Measured"),
                    ("estimated", "Estimated"),
                    ("N/A", "Not recorded / Not applicable"),
                ],
                default="meqsured",
                max_length=15,
                verbose_name="Is weight estimated or measured?",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="historicalvitals",
            name="bp_one_not_taken_reason",
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                verbose_name="If not done, please explain",
            ),
        ),
        migrations.AlterField(
            model_name="historicalvitals",
            name="bp_two_not_taken_reason",
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                verbose_name="If not done, please explain",
            ),
        ),
        migrations.AlterField(
            model_name="vitals",
            name="bp_one_not_taken_reason",
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                verbose_name="If not done, please explain",
            ),
        ),
        migrations.AlterField(
            model_name="vitals",
            name="bp_two_not_taken_reason",
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                verbose_name="If not done, please explain",
            ),
        ),
    ]
