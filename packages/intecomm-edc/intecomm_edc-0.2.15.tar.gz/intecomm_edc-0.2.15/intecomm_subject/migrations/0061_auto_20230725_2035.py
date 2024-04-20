# Generated by Django 4.2.3 on 2023-07-25 17:35
from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations
from edc_list_data import PreloadData
from tqdm import tqdm

from intecomm_lists.list_data import list_data


def update_next_appointment(apps, schema_editor):
    model_cls = apps.get_model("intecomm_subject", "nextappointment")
    infosources_model_cls = apps.get_model("edc_next_appointment", "infosources")

    ld = {
        "edc_next_appointment.infosources": list_data.get("edc_next_appointment.infosources")
    }
    PreloadData(list_data=ld, apps=apps)

    total = model_cls.objects.all().count()
    for obj in tqdm(model_cls.objects.all(), total=total):
        # info_source_new
        try:
            obj.info_source_id = infosources_model_cls.objects.get(name=obj.info_source_old).id
        except ObjectDoesNotExist as e:
            names = ",".join([obj.name for obj in infosources_model_cls.objects.all()])
            raise ObjectDoesNotExist(
                f"{e}. Expected one of {names}. Got '{obj.info_source_old}'. Perhaps run "
                "post-migrate to populate list model "
                f"{infosources_model_cls._meta.label_lower}. For example, run "
                "`migrate intecomm_subject 0060` followed by `migrate`."
            )
        obj.save_base(update_fields=["info_source_id"])


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_subject", "0060_historicalnextappointment_info_source_and_more"),
    ]

    operations = [migrations.RunPython(update_next_appointment)]
