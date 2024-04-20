# Generated by Django 4.2.3 on 2023-07-10 18:54

import django.core.validators
import django_crypto_fields.fields.encrypted_char_field
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_screening", "0045_alter_consentrefusal_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalpatientlog",
            name="legal_name",
            field=django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                blank=True,
                help_text=" (Encryption: RSA local)",
                max_length=71,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Ensure full name consists of letters only in upper case separated by single spaces",
                        regex="^(([A-Z]+ )*[A-Z]+)?$",
                    )
                ],
                verbose_name="Full name",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="legal_name",
            field=django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                blank=True,
                help_text=" (Encryption: RSA local)",
                max_length=71,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Ensure full name consists of letters only in upper case separated by single spaces",
                        regex="^(([A-Z]+ )*[A-Z]+)?$",
                    )
                ],
                verbose_name="Full name",
            ),
        ),
        migrations.AlterField(
            model_name="patientlog",
            name="legal_name",
            field=django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                blank=True,
                help_text=" (Encryption: RSA local)",
                max_length=71,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Ensure full name consists of letters only in upper case separated by single spaces",
                        regex="^(([A-Z]+ )*[A-Z]+)?$",
                    )
                ],
                verbose_name="Full name",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="legal_name",
            field=django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                blank=True,
                help_text=" (Encryption: RSA local)",
                max_length=71,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Ensure full name consists of letters only in upper case separated by single spaces",
                        regex="^(([A-Z]+ )*[A-Z]+)?$",
                    )
                ],
                verbose_name="Full name",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="patientlog",
            unique_together={("legal_name", "initials")},
        ),
        migrations.AlterUniqueTogether(
            name="subjectscreening",
            unique_together={("legal_name", "initials")},
        ),
    ]
