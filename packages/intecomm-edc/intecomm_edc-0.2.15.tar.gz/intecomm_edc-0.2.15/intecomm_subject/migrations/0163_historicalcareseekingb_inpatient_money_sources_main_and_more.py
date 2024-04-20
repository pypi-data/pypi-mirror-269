# Generated by Django 5.0.4 on 2024-04-10 22:15

import edc_model_fields.fields.custom_django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("intecomm_subject", "0162_alter_careseekingb_inpatient_cost_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalcareseekingb",
            name="inpatient_money_sources_main",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                choices=[
                    ("own_savings", "Own saving (e.g. “loose funds”, bank savings)"),
                    (
                        "family_gift",
                        "Loan from family members that does not need to be repaid",
                    ),
                    ("family_loan", "Loan from family member that needs to be repaid"),
                    (
                        "gift_relative",
                        "Loan from relative/neighbour that does not need to be repaid",
                    ),
                    ("loan_relative", "Loan from relative/neighbour that needs to be repaid"),
                    ("loan_money_lender", "Loan from money lender"),
                    ("loan_bank", "Loan from another source eg bank"),
                    ("community", "Self-help community group"),
                    ("national_insurance", "National health insurance"),
                    ("private_insurance", "Private health insurance"),
                    ("community_insurance", "Community health insurance"),
                    ("waiver", "Government waiver"),
                    (
                        "asset_sale",
                        "Sale of assets (property, livestock, jewellery, household goods, etc)",
                    ),
                    ("OTHER", "Other (specify)"),
                ],
                max_length=25,
                metadata="FINSOURCEMAIN1",
                null=True,
                verbose_name="Of the various sources that you have just mentioned, what was the main source of payment?",
            ),
        ),
        migrations.RemoveField(
            model_name="careseekingb",
            name="inpatient_money_sources_main",
        ),
        migrations.AddField(
            model_name="careseekingb",
            name="inpatient_money_sources_main",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                choices=[
                    ("own_savings", "Own saving (e.g. “loose funds”, bank savings)"),
                    (
                        "family_gift",
                        "Loan from family members that does not need to be repaid",
                    ),
                    ("family_loan", "Loan from family member that needs to be repaid"),
                    (
                        "gift_relative",
                        "Loan from relative/neighbour that does not need to be repaid",
                    ),
                    ("loan_relative", "Loan from relative/neighbour that needs to be repaid"),
                    ("loan_money_lender", "Loan from money lender"),
                    ("loan_bank", "Loan from another source eg bank"),
                    ("community", "Self-help community group"),
                    ("national_insurance", "National health insurance"),
                    ("private_insurance", "Private health insurance"),
                    ("community_insurance", "Community health insurance"),
                    ("waiver", "Government waiver"),
                    (
                        "asset_sale",
                        "Sale of assets (property, livestock, jewellery, household goods, etc)",
                    ),
                    ("OTHER", "Other (specify)"),
                ],
                max_length=25,
                metadata="FINSOURCEMAIN1",
                null=True,
                verbose_name="Of the various sources that you have just mentioned, what was the main source of payment?",
            ),
        ),
    ]
