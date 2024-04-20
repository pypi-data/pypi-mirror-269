from edc_sites.site import sites

from intecomm_lists.constants import HC_III, HC_IV

from .intecomm_site import IntecommSite

fqdn = "intecomm.clinicedc.org"

ug_language_codes = ["en", "lg", "ry", "sw"]
tz_language_codes = ["en", "sw", "mas"]


sites.register(
    IntecommSite(
        101,
        "kasangati",
        country_code="ug",
        country="uganda",
        language_codes=ug_language_codes,
        health_facility_type=HC_IV,
        domain=f"kasangati.ug.{fqdn}",
    ),
    IntecommSite(
        102,
        "kisugu",
        health_facility_type=HC_III,
        country_code="ug",
        country="uganda",
        language_codes=ug_language_codes,
        domain=f"kisugu.ug.{fqdn}",
    ),
    IntecommSite(
        103,
        "kiswa",
        health_facility_type=HC_III,
        country_code="ug",
        country="uganda",
        language_codes=ug_language_codes,
        domain=f"kiswa.ug.{fqdn}",
    ),
    IntecommSite(
        104,
        "kyazanga",
        health_facility_type=HC_IV,
        country_code="ug",
        country="uganda",
        language_codes=ug_language_codes,
        domain=f"kyazanga.ug.{fqdn}",
    ),
    IntecommSite(
        105,
        "mpigi",
        health_facility_type=HC_IV,
        country_code="ug",
        country="uganda",
        language_codes=ug_language_codes,
        domain=f"mpigi.ug.{fqdn}",
    ),
    IntecommSite(
        106,
        "namayumba",
        health_facility_type=HC_III,
        country_code="ug",
        country="uganda",
        language_codes=ug_language_codes,
        domain=f"namayumba.ug.{fqdn}",
    ),
    IntecommSite(
        107,
        "namulonge",
        health_facility_type=HC_III,
        country_code="ug",
        country="uganda",
        language_codes=ug_language_codes,
        domain=f"namulonge.ug.{fqdn}",
    ),
    IntecommSite(
        108,
        "ndejje",
        health_facility_type=HC_IV,
        country_code="ug",
        country="uganda",
        language_codes=ug_language_codes,
        domain=f"ndejje.ug.{fqdn}",
    ),
    IntecommSite(
        109,
        "sekiwunga",
        health_facility_type=HC_III,
        country_code="ug",
        country="uganda",
        language_codes=ug_language_codes,
        domain=f"sekiwunga.ug.{fqdn}",
    ),
    IntecommSite(
        110,
        "wakiso",
        health_facility_type=HC_IV,
        country_code="ug",
        country="uganda",
        language_codes=ug_language_codes,
        domain=f"wakiso.ug.{fqdn}",
    ),
    IntecommSite(
        201,
        "amana",
        health_facility_type=HC_IV,
        title="Amana Hospital",
        country="tanzania",
        country_code="tz",
        language_codes=tz_language_codes,
        domain=f"amana.tz.{fqdn}",
    ),
    IntecommSite(
        202,
        "bagamoyo",
        health_facility_type=HC_IV,
        title="Bagamoyo Regional Hospital",
        country="tanzania",
        country_code="tz",
        language_codes=tz_language_codes,
        domain=f"bagamoyo.tz.{fqdn}",
    ),
    IntecommSite(
        203,
        "rugambwa",
        health_facility_type=HC_IV,
        title="Cardinal Rugambwa Hospital",
        country="tanzania",
        country_code="tz",
        language_codes=tz_language_codes,
        domain=f"rugambwa.tz.{fqdn}",
    ),
    IntecommSite(
        204,
        "hindu_mandal",
        health_facility_type=HC_IV,
        title="Hindu Mandal Hospital",
        country="tanzania",
        country_code="tz",
        language_codes=tz_language_codes,
        domain=f"hindu-mandal.tz.{fqdn}",
    ),
    IntecommSite(
        205,
        "kisarawe",
        health_facility_type=HC_IV,
        title="Kisarawe District Hospital",
        country="tanzania",
        country_code="tz",
        language_codes=tz_language_codes,
        domain=f"kisarawe.tz.{fqdn}",
    ),
    IntecommSite(
        206,
        "mbagala",
        health_facility_type=HC_III,
        title="Mbagala Hospital",
        country="tanzania",
        country_code="tz",
        language_codes=tz_language_codes,
        domain=f"mbagala.tz.{fqdn}",
    ),
    IntecommSite(
        207,
        "mnazi_moja",
        health_facility_type=HC_III,
        title="Mnazi Moja Hospital",
        country="tanzania",
        country_code="tz",
        language_codes=tz_language_codes,
        domain=f"mnazi.tz.{fqdn}",
    ),
    IntecommSite(
        208,
        "mwananyamala",
        health_facility_type=HC_IV,
        title="Mwananyamala Hospital",
        country="tanzania",
        country_code="tz",
        language_codes=tz_language_codes,
        domain=f"mwananyamala.tz.{fqdn}",
    ),
    IntecommSite(
        209,
        "sinza",
        health_facility_type=HC_III,
        title="Sinza Hospital",
        country_code="tz",
        country="tanzania",
        language_codes=tz_language_codes,
        domain=f"sinza.tz.{fqdn}",
    ),
    IntecommSite(
        210,
        "temeke",
        health_facility_type=HC_IV,
        title="Temeke Hospital",
        country="tanzania",
        country_code="tz",
        language_codes=tz_language_codes,
        domain=f"temeke.tz.{fqdn}",
    ),
)
