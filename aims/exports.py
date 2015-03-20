import unicodecsv
import xlwt
from datetime import date

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.utils.translation import get_language
from django.conf import settings
from django.db.models import Sum

from aims import base_utils
from aims import models as aims


def org_title(activity):
    if not activity['reporting_organisation_id']:
        return ""
    if activity['reporting_organisation__name']:
        return activity['reporting_organisation__name']
    if activity['reporting_organisation__name']:
        return activity['reporting_organisation__name']
    if activity['reporting_organisation_id']:
        return activity['reporting_organisation_id']


def some_sectors(sectors):
    out_sectors = []
    for s in sectors:
        percentage = s['percentage']
        if s['sector__name'] is None:
            sector = base_utils.UNKNOWN_SECTOR_NAME
        else:
            sector = s['sector__name']
        if percentage is None:
            percentage = base_utils.UNKNOWN_PERCENTAGE
        else:
            percentage = "%.2f" % percentage
        out_sectors.append("%s %s%%" % (unicode(sector), percentage))
    return "|".join(out_sectors)


def activity_objective(objectives, activity, preferred_language=None):
    if activity not in objectives:
        return ""
    if len(objectives[activity]) == 1:
        return objectives[activity][0]['description']

    objectives = objectives[activity]

    # preferred language
    for objective in objectives:
        if preferred_language and objective['language_id'] and objective['language_id'] == preferred_language:
            return objective['description']

    # default language
    for objective in objectives:
        if objective['language_id'] and objective['language_id'] in settings.LANGUAGE_CODE:
            return objective['description']
    # first objective
    return objectives[0]['description']


def some_title(titles, preferred_language=None):
    if len(titles) < 1:
        return unicode(_("no title"))
    if len(titles) == 1:
        return titles[0]['title']

    # preferred language
    for title in titles:
        if preferred_language and title['language_id'] and title['language_id'] == preferred_language:
            return title['title']

    # default language
    for title in titles:
        if title['language_id'] and title['language_id'] in settings.LANGUAGE_CODE:
            return title['title']
    # first title
    return titles[0]['title']


def some_description(descriptions, preferred_language=None):
    if len(descriptions) < 1:
        return unicode(_("no description"))
    if len(descriptions) == 1:
        return descriptions[0]['description']

    # preferred language
    for description in descriptions:
        if preferred_language and description['language_id'] and description['language_id'] == preferred_language:
            return description['description']

    # default language
    for description in descriptions:
        if description['language_id'] and description['language_id'] in settings.LANGUAGE_CODE:
            return description['description']

    # first description
    return descriptions[0]['description']


def some_organisations(organisations):
    return '| '.join(list(set([org['organisation__name'] for org in organisations])))


def export_activities(activities):
    """
       ACTIVITY ID, TITLE, SECTOR, STATUS, TOTAL BUDGET,
       REPORTING ORGANIZATION, START DATE, END DATE
        CONTACT.name, CONTACT.telephone, CONTACT.email
        - reporting org: show the name (or abbrev if none or code if none)
        - status : show the status name
        - show the sector names and their percents
        - multiple sectors in the same column (until I know different)
    """
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    today = date.today()
    response['Content-Disposition'] = 'attachment; filename=activities_%s.xls' % today.strftime('%Y_%m_%d')
    #writer = unicodecsv.writer(response, delimiter=',')

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("Activities")

    # Commente out for now as it prevents Numbers (and Excel?) from puting the data in their proper columns
    # header = [unicode(_('Filtered activities')), today.strftime('%Y/%m/%d')]
    # writer.writerow(header)

    columns = [
        unicode(_("id")),
        unicode(_("Title")),
        unicode(_('Description')),
        unicode(_('Objective')),
        unicode(_("Sector")),
        unicode(_('Sector Working Group')),
        unicode(_("Status")),
        unicode(_("Collaboration Type")),
        unicode(_("Default Finance Type")),
        unicode(_("Default Aid Type")),
        unicode(_("Default Flow Type")),
        unicode(_("Default Currency")),
        unicode(_("Total Budget")),
        unicode(_("Total Disbursement")),
        unicode(_("Total Budget USD")),
        unicode(_("Total Disbursement USD")),
        unicode(_("Reporting Organisation")),
        unicode(_("Financing")),
        unicode(_('Extending')),
        unicode(_('Implementing')),
        unicode(_('Partner Ministry')),
        unicode(_('State/Region')),
        unicode(_('Township')),
        unicode(_("Planned Start date")),
        unicode(_("Planned End date")),
        unicode(_("Actual Start date")),
        unicode(_("Actual End date")),
        unicode(_("Contact Name")),
        unicode(_("Contact Phone")),
        unicode(_("Contact Email")),
    ]

    #writer.writerow(["%s" % x for x in columns])
    for i in range(len(columns)):
        sheet.write(0, i, columns[i])
    # print "Exporter: Should filter activity title name by language"

    current_language = get_language()

    sectors_activities = {}
    for sector in aims.activity_sector.objects.select_related('sector').exclude(vocabulary_id='RO')\
            .values('activity_id', 'sector__name', 'percentage'):
        if sector['activity_id'] not in sectors_activities:
            sectors_activities[sector['activity_id']] = []
        sectors_activities[sector['activity_id']].append(sector)

    national_sectors_activities = {}
    for sector in aims.activity_sector.objects.select_related('sector').filter(vocabulary_id='RO')\
            .values('activity_id', 'sector__name', 'percentage'):
        if sector['activity_id'] not in national_sectors_activities:
            national_sectors_activities[sector['activity_id']] = []
        national_sectors_activities[sector['activity_id']].append(sector)

    titles_activities = {}
    for title in aims.title.objects.values('activity_id', 'title', 'language_id'):
        if title['activity_id'] not in titles_activities:
            titles_activities[title['activity_id']] = []
        titles_activities[title['activity_id']].append(title)

    desc_activities = {}
    for description in aims.description.objects.values('activity_id', 'description', 'language_id'):
        if description['activity_id'] not in desc_activities:
            desc_activities[description['activity_id']] = []
        desc_activities[description['activity_id']].append(description)

    objectives = {}
    for objective in aims.description.objects.filter(type_id=2).values('activity_id', 'description', 'language_id'):
        if objective['activity_id'] not in objectives:
            objectives[objective['activity_id']] = []
        objectives[objective['activity_id']].append(objective)

    organisations = {}
    organisation_set = aims.activity_participating_organisation.objects.select_related('organisation')\
        .values('activity_id', 'role_id', 'organisation__name')

    for organisation in organisation_set:
        if organisation['activity_id'] not in organisations:
            organisations[organisation['activity_id']] = {}
        if organisation['role_id'] not in organisations[organisation['activity_id']]:
            organisations[organisation['activity_id']][organisation['role_id']] = []
        organisations[organisation['activity_id']][organisation['role_id']].append(organisation)

    location_activities = {}
    for location in aims.location.objects.values('activity_id', 'adm_country_adm1', 'adm_country_adm2', 'percentage'):
        if location['activity_id'] not in location_activities:
            location_activities[location['activity_id']] = []
        location_activities[location['activity_id']].append(location)

    contact_activities = {}
    for contact in aims.contact_info.objects.values('activity_id', 'person_name', 'telephone', 'email'):
        if contact['activity_id'] not in contact_activities:
            contact_activities[contact['activity_id']] = []
        contact_activities[contact['activity_id']].append(contact)

    outcomes_activities = {}
    for outcome in aims.result.objects.filter(result_type__name="Outcome")\
            .values('activity_id', 'title', 'description'):
        if outcome['activity_id'] not in outcomes_activities:
            outcomes_activities[outcome['activity_id']] = []
        outcomes_activities[outcome['activity_id']].append(outcome)

    total_disbursement_in_dollars = {total['activity_id']: total['transaction_value_for_location__dollars__sum']
                                     for total in aims.transaction.objects.filter(transaction_type__code='D')
                                     .values('activity_id')
                                     .annotate(Sum('transaction_value_for_location__dollars'))}

    total_disbursement = {total['activity_id']: total['value__sum']
                          for total in aims.transaction.objects.filter(transaction_type__code='D')
                          .values('activity_id')
                          .annotate(Sum('value'))}

    budget_in_dollars = {total['activity_id']: total['dollars']
                         for total in aims.ActivityTotalBudgetUSD.objects.values('activity_id', 'dollars')}

    activities = activities.values('pk',
                                   'activity_status__name',
                                   'reporting_organisation_id',
                                   'reporting_organisation__name',
                                   'reporting_organisation__abbreviation',
                                   'collaboration_type__name',
                                   'default_finance_type__name',
                                   'default_aid_type__name',
                                   'default_flow_type__name',
                                   'start_planned',
                                   'end_planned',
                                   'start_actual',
                                   'end_actual',
                                   'total_budget',
                                   'total_budget_currency_id',
                                   )

    for index, activity in enumerate(activities):
        sectors = some_sectors(sectors_activities[activity['pk']]) if activity['pk'] in sectors_activities else ""
        title = some_title(titles_activities[activity['pk']], current_language)\
            if activity['pk'] in titles_activities else ""
        description = some_description(desc_activities[activity['pk']], current_language) \
            if activity['pk'] in desc_activities else ""
        reporting_org = org_title(activity)

        if activity['pk'] in contact_activities:
            contact = contact_activities[activity['pk']][0]
            contact_name = contact['person_name'] if contact['person_name'] else ""
            contact_phone = contact['telephone'] if contact['telephone'] else ""
            contact_email = contact['email'] if contact['email'] else ""
        else:
            contact_name, contact_phone, contact_email = "", "", ""

        try:
            financing_organisation = some_organisations(organisations[activity['pk']]["Funding"])
        except:
            financing_organisation = ""

        try:
            extending_organisation = some_organisations(organisations[activity['pk']]["Extending"])
        except:
            extending_organisation = ""

        try:
            implimenting_organisation = some_organisations(organisations[activity['pk']]["Implementing"])
        except:
            implimenting_organisation = ""

        try:
            sector_working_group = some_sectors(national_sectors_activities[activity['pk']])
        except:
            sector_working_group = ""

        try:
            ministry = some_organisations(organisations[activity['pk']]["Accountable"])
        except:
            ministry = ""

        if activity['pk'] in outcomes_activities:
            outcomes = outcomes_activities[activity['pk']]
            outcome = " | ".join([outcome['description'] for outcome in outcomes if outcome['description']])
        else:
            outcome = ""

        if activity['pk'] in location_activities:
            locations = location_activities[activity['pk']]
            # locations = [(location.adm_country_adm1, location.adm_country_adm2) for location in locations]
            # location = " | ".join([("%s - %s") % location for location in locations])
            distinct_regions = set(location['adm_country_adm1'] for location in locations)
            states_regions = []
            for region in distinct_regions:
                if region:
                    states_regions.append("{reg} - {pct}%".format(
                        reg=region,
                        pct=locations[0]['percentage'] or 100.0,))
            state_region = " | ".join([state_region for state_region in states_regions])

            distinct_townships = set(location['adm_country_adm2'] for location in locations)
            townships = []
            for region in distinct_townships:
                if region:
                    townships.append("{reg} - {pct}%".format(
                        reg=region,
                        pct=locations[0]['percentage'] or 100.0,))
            township = " | ".join([township for township in townships])
        else:
            # location = ""
            state_region = ""
            township = ""

        if activity['activity_status__name']:
            activity_status_name = activity['activity_status__name']
        else:
            activity_status_name = ""

        if activity['total_budget']:
            if not activity['total_budget_currency_id']:
                total_budget_in_dollars = activity['total_budget']
            else:
                total_budget_in_dollars = budget_in_dollars[activity['pk']]\
                    if activity['pk'] in budget_in_dollars else 0
        else:
            total_budget_in_dollars = 0

        disbursement_in_dollars = total_disbursement_in_dollars[activity['pk']]\
            if activity['pk'] in total_disbursement_in_dollars else ""

        disbursement = total_disbursement[activity['pk']]\
            if activity['pk'] in total_disbursement else ""

        objective = activity_objective(objectives, activity['pk'], current_language)

        line = [
            "%s" % activity['pk'],
            "%s" % title,
            "%s" % description,
            "%s" % objective,
            "%s" % sectors,
            "%s" % sector_working_group,
            "%s" % activity_status_name,
            "%s" % str(activity['collaboration_type__name']) if activity['collaboration_type__name'] else "",
            "%s" % str(activity['default_finance_type__name']) if activity['default_finance_type__name'] else "",
            "%s" % str(activity['default_aid_type__name']) if activity['default_aid_type__name'] else "",
            "%s" % str(activity['default_flow_type__name']) if activity['default_flow_type__name'] else "",
            "%s" % str(activity['total_budget_currency_id']),
            "%s" % str(activity['total_budget']),
            "%s" % disbursement if disbursement else 0,
            "%s" % total_budget_in_dollars,
            "%s" % disbursement_in_dollars if disbursement_in_dollars else 0,
            "%s" % reporting_org,
            "%s" % financing_organisation,
            "%s" % extending_organisation,
            "%s" % implimenting_organisation,
            "%s" % ministry,
            "%s" % state_region,
            "%s" % township,
            "%s" % (activity['start_planned'] or ""),
            "%s" % (activity['end_planned'] or ""),
            "%s" % (activity['start_actual'] or ""),
            "%s" % (activity['end_actual'] or ""),
            "%s" % contact_name,
            "%s" % contact_phone,
            "%s" % contact_email,
        ]

        for i in range(len(line)):
            sheet.write(index+1, i, line[i])

    workbook.save(response)

    return response
