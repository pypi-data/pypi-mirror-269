# Generated by Django 4.2.3 on 2023-07-26 13:31

from django.db import migrations
from tqdm import tqdm


def update_health_talk(apps, schema_editor):
    """Update healthfacility FK from old healthfacility model to
    new healthfacility model.
    """
    model_cls = apps.get_model("intecomm_screening", "healthtalklog")
    healthfacility_new_model_cls = apps.get_model("intecomm_facility", "healthfacility")
    healthfacility_old_model_cls = apps.get_model("intecomm_screening", "oldhealthfacility")
    total = model_cls.objects.all().count()
    print("\n")
    for obj in tqdm(model_cls.objects.all(), total=total):
        if not obj.old_health_facility:
            continue
        old_health_facility = healthfacility_old_model_cls.objects.get(
            id=obj.old_health_facility
        )
        obj.health_facility_id = healthfacility_new_model_cls.objects.get(
            name=old_health_facility.name
        ).id
        obj.save_base(update_fields=["health_facility_id"])
    print("\n")


class Migration(migrations.Migration):
    dependencies = [
        # ("intecomm_facility", "0002_alter_healthfacility_device_created_and_more"),
        (
            "intecomm_screening",
            "0050_delete_healthfacility_healthtalklog_health_facility_and_more",
        ),
        ("intecomm_subject", "0067_auto_20230726_0008"),
    ]

    operations = [migrations.RunPython(update_health_talk)]
