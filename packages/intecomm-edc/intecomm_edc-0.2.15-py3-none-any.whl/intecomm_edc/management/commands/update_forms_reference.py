import os
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.color import color_style

style = color_style()


def update_forms_reference(sender=None, **kwargs):
    from edc_form_describer import FormsReference

    from intecomm_subject.admin_site import intecomm_subject_admin
    from intecomm_visit_schedule.visit_schedules import visit_schedule

    sys.stdout.write(
        style.MIGRATE_HEADING("Refreshing CRF reference document for intecomm_subject\n")
    )
    doc_folder = os.path.join(settings.BASE_DIR, "docs")
    if not os.path.exists(doc_folder):
        os.mkdir(doc_folder)
    forms = FormsReference(
        visit_schedules=[visit_schedule],
        admin_site=intecomm_subject_admin,
        title="INTECOMM-EDC Forms Reference",
        add_per_form_timestamp=False,
    )
    path = os.path.join(doc_folder, "forms_reference.md")
    forms.to_file(path=path, overwrite=True)


class Command(BaseCommand):
    help = "Update forms reference document (.md)"

    def handle(self, *args, **options):
        update_forms_reference()
