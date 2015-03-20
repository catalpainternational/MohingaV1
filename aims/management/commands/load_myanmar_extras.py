from django.core.management.base import BaseCommand

from IATI import models as iati
from aims import models as aims


class Command(BaseCommand):

    def handle(self, *args, **options):
        create_sectors()
        create_ministries()
        create_sector_working_groups()
        adjust_organisations()
        adjust_transactions()

def create_sectors():
    for i in range(17):
        name = "MM - " + str(i)
        sector = iati.sector(code=55000 + i, name=name, description="Myanmar National Sector "+name)
        sector.save()
        sector


def create_sector_working_groups():
    other_public_sector_type = iati.organisation_type.objects.get(name='Other Public Sector')
    for i in range(17):
        name = "MM-FERD-SWG" + str(i)
        swg = iati.organisation(code=name, abbreviation=name, name=name, reported_by_organisation="FERD", type=other_public_sector_type)
        swg.save()


def create_ministries():
    gov_org_type = iati.organisation_type.objects.get(name='Government')
    for i in range(36):
        name = "MM-FERD-MIN" + str(i)
        ministry = iati.organisation(code=name, abbreviation=name, name=name, reported_by_organisation="FERD", type=gov_org_type)
        ministry.save()


def adjust_organisations():
    activities = aims.activity.objects.all()
    for activity in activities:
        if aims.activity_participating_organisation.objects.filter(activity=activity, role="Extending").count() > 1:
            orgs = aims.activity_participating_organisation.objects.filter(activity=activity, role="Extending")
            if list(orgs).count(orgs[0]) == 2:
                orgs.remove(orgs[0])


def adjust_transactions():

    trans = aims.transaction.objects.filter(receiver_organisation=None)
    for tran in trans:
        if tran.activity.participating_organisation.filter(activity_participating_organisation__role="Extending").count() > 0:
            tran.receiver_organisation = tran.activity.participating_organisation.filter(activity_participating_organisation__role="Extending").first()
            tran.save()

    trans = aims.transaction.objects.filter(value_date=None)
    for tran in trans:
        if tran.activity.start_actual:
            tran.transaction_date = tran.value_date = tran.activity.start_actual
        elif tran.activity.start_planned:
            tran.transaction_date = tran.value_date = tran.activity.start_planned
        else:
            pass
        tran.save()

    trans = aims.transaction.objects.filter(provider_organisation=None)
    for tran in trans:
        if tran.activity.participating_organisation.filter(activity_participating_organisation__role="Funding").count() > 0:
            tran.provider_organisation = tran.activity.participating_organisation.get(activity_participating_organisation__role="Funding")
            tran.save()
