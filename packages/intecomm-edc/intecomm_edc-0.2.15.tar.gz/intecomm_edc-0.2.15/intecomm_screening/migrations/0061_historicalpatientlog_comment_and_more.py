# Generated by Django 4.2.4 on 2023-08-31 02:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_screening", "0060_historicalpatientlogug"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalpatientlog",
            name="comment",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="historicalpatientlogug",
            name="comment",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="patientlog",
            name="comment",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
