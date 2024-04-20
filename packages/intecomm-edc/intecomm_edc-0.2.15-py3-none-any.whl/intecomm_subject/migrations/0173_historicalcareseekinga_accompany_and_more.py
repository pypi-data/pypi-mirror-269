# Generated by Django 5.0.4 on 2024-04-16 13:32

import edc_model_fields.fields.custom_django_fields
import intecomm_subject.models.fields.expense_field
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("intecomm_subject", "0172_alter_careseekingb_inpatient_cost_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalcareseekinga",
            name="accompany",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                choices=[
                    ("alone", "No one, I came alone"),
                    ("main_earner", "Main household earner"),
                    ("adult", "Other family member/relatives/friends (adults)"),
                    ("child", "Other family member/relatives/friends (children)"),
                ],
                max_length=25,
                metadata="FACMP1",
                null=True,
                verbose_name="Who accompanied you here today?",
            ),
        ),
        migrations.RemoveField(
            model_name="careseekinga",
            name="accompany",
        ),
        migrations.AlterField(
            model_name="careseekinga",
            name="travel_cost",
            field=intecomm_subject.models.fields.expense_field.ExpenseField(
                metadata="FTRAVCOST1",
                null=True,
                verbose_name="Thinking about yourself and anyone that accompanied you, how much was spent on travel from your home to reach here?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekinga",
            name="travel_cost",
            field=intecomm_subject.models.fields.expense_field.ExpenseField(
                metadata="FTRAVCOST1",
                null=True,
                verbose_name="Thinking about yourself and anyone that accompanied you, how much was spent on travel from your home to reach here?",
            ),
        ),
        migrations.AddField(
            model_name="careseekinga",
            name="accompany",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                choices=[
                    ("alone", "No one, I came alone"),
                    ("main_earner", "Main household earner"),
                    ("adult", "Other family member/relatives/friends (adults)"),
                    ("child", "Other family member/relatives/friends (children)"),
                ],
                max_length=25,
                metadata="FACMP1",
                null=True,
                verbose_name="Who accompanied you here today?",
            ),
        ),
    ]
