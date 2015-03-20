import re
import datetime
from django.db.models import Count, Sum

from aims import models as aims
from aims import base_utils


def activity_statuses(activity_queryset=None):
    '''
    aid_by: sector
    '''
    if activity_queryset is None:
        activity_queryset = aims.activity.objects.all()
    activity_queryset = list(activity_queryset)
    activity_statuses = aims.activity_status.objects.filter(activity__in=activity_queryset)\
                                                    .values('name', 'code')\
                                                    .annotate(value=Count('activity'))

    activity_statuses = unicode(activity_statuses).replace(" u'", " '")

    return activity_statuses


def total_commitments(transaction_queryset=None, activity_sector_queryset=None, activity_statuses=[2, ]):
    '''
    aid_by: sector
            donor
            ministry
            location
    '''

    if transaction_queryset is None:
        transaction_queryset = aims.transaction.objects

    if activity_sector_queryset is not None:
        transaction_queryset = transaction_queryset.filter(transaction_type="C", activity__activity_status__code=2)
        total_activities = activity_sector_queryset.count()
        aggregate_percentage = activity_sector_queryset.aggregate(Sum('percentage'))['percentage__sum'] or 0
        total_commitments = transaction_queryset.aggregate(Sum('value_in__dollars'))['value_in__dollars__sum']
        total_commitments = float(total_commitments) * (float(aggregate_percentage) / total_activities / 100) if total_commitments else 0
    else:
        total_commitments = transaction_queryset.filter(transaction_type="C", activity__activity_status__code__in=activity_statuses)\
                                                .aggregate(Sum('value_in__dollars'))
        total_commitments = total_commitments['value_in__dollars__sum']

    return total_commitments


def total_disbursements(transaction_queryset=None, activity_statuses=[2, ]):
    '''
    aid_by: sector
            donor
            ministry
            location
    '''
    if transaction_queryset is None:
        transaction_queryset = aims.transaction.objects

    total_disbursements = transaction_queryset.filter(transaction_type="D", activity__activity_status__code__in=activity_statuses)\
                                              .aggregate(Sum('value_in__dollars'))
    total_disbursements = total_disbursements['value_in__dollars__sum'] if total_disbursements['value_in__dollars__sum'] else 0

    return total_disbursements


def donor_commitments(transaction_queryset=None, limit=20, activity_statuses=[2, ]):
    '''
    aid_by: sector
            donor
            ministry
    '''

    if transaction_queryset is None:
        transaction_queryset = aims.transaction.objects
    donor_commitments = transaction_queryset.filter(transaction_type='C', activity__activity_status__code__in=activity_statuses)\
                                            .values('provider_organisation__abbreviation', 'provider_organisation__name'
                                                , 'provider_organisation__code')\
                                            .annotate(Sum('value_in__dollars'))\
                                            .order_by('-value_in__dollars__sum')[:limit]

    donor_commitments = [{'name': donor['provider_organisation__abbreviation'] or donor['provider_organisation__name'] or 'Unidentified',
                          'value': donor['value_in__dollars__sum'],
                          'code': donor['provider_organisation__code'] or base_utils.UNKNOWN_DONOR_CODE,
                          'pretty': base_utils.prettify_compact(donor['value_in__dollars__sum'])}
                          for donor in donor_commitments]

    donor_commitments = unicode(donor_commitments).replace(" u'", " '")

    return donor_commitments


def percent_disbursed(total_commitments, total_disbursements):
    '''
    aid_by: sector
            donor
            location
    '''

    if total_commitments is None:
        total_commitments = 0

    if total_disbursements is None:
        total_disbursements = 0

    if total_commitments > 0:
        percent_disbursed = (100* (total_disbursements / total_commitments)) if total_disbursements else 0
    else:
        percent_disbursed = 100 if total_disbursements > 0 else 0

    return percent_disbursed


def activities_by_ministry(activity_queryset=None, limit=3):
    '''
    aid_by: sector
            donor
            ministry
            location
    '''
    if activity_queryset is None:
        activity_queryset = aims.activity.objects.all()
    activity_queryset = list(activity_queryset)
    activities_by_ministry = aims.activity_participating_organisation.objects.filter(activity__in=activity_queryset, role='Accountable')\
                                                                             .exclude(organisation=None)\
                                                                             .values('organisation__name', 'organisation__code')\
                                                                             .annotate(value=Count('activity'), dollars=Sum('activity__transaction__value_in__dollars'))\
                                                                             .order_by('-value')

    top_three = activities_by_ministry[:limit] if limit is not None else activities_by_ministry

    # the_rest_value = sum([item['value'] for item in activities_by_ministry[limit:]])
    # the_rest_dollars = sum([item['dollars'] for item in activities_by_ministry[limit:] if item['dollars']])
    # the_rest = {'code': 4, 'name': 'Other', 'value': the_rest_value, 'pretty': base_utils.prettify_compact(the_rest_dollars)}

    activities_by_ministry = [{'code': ministry['organisation__code'],
                               'name': re.sub("ministry of", "", ministry['organisation__name'], flags=re.IGNORECASE).strip(),
                               'value': ministry['value'],
                               'pretty': ministry['value']}\
                               #'pretty': base_utils.prettify_compact(ministry['dollars'])}\
                                for code, ministry in enumerate(top_three)]

    # activities_by_ministry.append(the_rest)
    activities_by_ministry = unicode(activities_by_ministry).replace(" u'", " '")
    activities_by_ministry = unicode(activities_by_ministry).replace(" u\"", " \"")

    return activities_by_ministry


def commitment_by_category(transaction_queryset=None, activity_sector_queryset=None, limit=3, activity_statuses=[2, ], json=True):
    '''
    aid_by: sector
            donor

    We get the total commitment
    Then we get the total number of activities
    We get the Sum of all the percentages by category
        divide that sum by the total number of activities and call it category_percent

    for each of the categories we multiply the total commitment by the category_percent
    '''

    commitment_by_category = []

    if transaction_queryset is None:
        transaction_queryset = aims.transaction.objects
    if not activity_sector_queryset:
        activity_sector_queryset = aims.activity_sector.objects

    for category in aims.sector_category.objects.exclude(code__startswith=550):

        total_commitment_sector = 0
        activity_sectors = activity_sector_queryset.filter(sector__code__startswith=category.code).exclude(vocabulary__code='RO')

        for activity_sector in activity_sectors:

            transactions = transaction_queryset.filter(activity=activity_sector.activity,
                                                        activity__activity_status__code__in=activity_statuses, 
                                                        transaction_type='C')

            if transactions:
                total_commitments = transactions.aggregate(Sum('value_in__dollars'))['value_in__dollars__sum']
                total_commitment_sector += (float(total_commitments or 0) * float(activity_sector.percentage or 0)) / 100

        if total_commitment_sector:
            commitment = {'name': re.sub(" and ", " & ", category.name, flags=re.IGNORECASE),
                          'value': total_commitment_sector,
                          'pretty': base_utils.prettify_compact(total_commitment_sector),
                          'code': int(category.code)}

            commitment_by_category.append(commitment)


        # transactions = transaction_queryset.filter(activity__activity_sector__sector__code__startswith=category.code, activity__activity_status__code=2, transaction_type='C')
        # activity_sectors = activity_sector_queryset.filter(sector__code__startswith=category.code)
        # total_activities = activity_sectors.count()

        # if total_activities and transactions:
        #     aggregate_percentage = activity_sectors.aggregate(Sum('percentage'))['percentage__sum']
        #     total_commitments = transactions.aggregate(Sum('value_in__dollars'))['value_in__dollars__sum']
        #     total_commitments = float(total_commitments) * (float(aggregate_percentage) / total_activities / 100)

        #     commitment = {'name': re.sub(" and ", " & ", category.name, flags=re.IGNORECASE),
        #                   'value': total_commitments,
        #                   'pretty': base_utils.prettify_compact(total_commitments),
        #                   'code': int(category.code)}

        #     commitment_by_category.append(commitment)

    commitment_by_category = sorted(commitment_by_category, key=lambda item: item['value'], reverse=True)

    if json:
        commitment_by_category = sorted(commitment_by_category, key=lambda category: category['value'], reverse=True)[:limit]
        commitment_by_category = unicode(commitment_by_category).replace(" u'", " '").replace(' u"', ' "')

    return commitment_by_category


def commitments_by_state(activity_queryset, states_queryset):
    '''
    aid_by: state
    '''
    states = states_queryset.values('st', 'st_pcode')
    states_dict = {state['st'].lower(): state['st_pcode'] for state in states}
    commitments_by_location = {state['st_pcode']: 0 for state in states}

    activity_queryset = list(activity_queryset)
    locations = aims.TransactionValueLocation.objects.filter(activity__in=activity_queryset,
                                                                transaction__transaction_type='C')\
                                            .exclude(location__adm_country_adm1__contains="Nation-wide")\
                                            .exclude(location__adm_country_adm1=None)\
                                            .values('location__adm_country_adm1')\
                                            .annotate(dollars=Sum('dollars'))

    for location in locations:
        commitments_by_location[states_dict[location['location__adm_country_adm1'].lower()]] = base_utils.prettify_compact(location['dollars'])
        commitments_by_location[states_dict[location['location__adm_country_adm1'].lower()] + '_natural'] = location['dollars']

    commitments_by_location = unicode(commitments_by_location).replace("u'", "'")

    return commitments_by_location

def commitments_percentage_by_state(activity, json=True):

    commitments_by_location = []

    locations = aims.TransactionValueLocation.objects.filter(activity=activity)\
                            .filter(transaction__transaction_type='C')\
                            .exclude(location__adm_country_adm1=None)\
                            .exclude(location__adm_country_adm1__contains="Nation-wide")\
                            .values('location__adm_country_adm1', 'location__adm_country_adm2', 'location__percentage')\
                            .annotate(dollars=Sum('dollars'))

    commitment_by_states = []
    for location in locations:
        commitment_by_states.append({
                'name': location['location__adm_country_adm2'] if location['location__adm_country_adm2'] else location['location__adm_country_adm1'],
                'percentage': location['location__percentage'],
                'total': base_utils.prettify_compact(location['dollars'])
            })

    if json:
        commitment_by_states = unicode(commitment_by_states).replace("u'", "'")

    return commitment_by_states


def commitments_by_township(activity_queryset, township_queryset):
    '''
    aid_by: township
    '''
    townships = township_queryset.values('ts', 'ts_pcode')
    township_dict = {township['ts'].lower(): township['ts_pcode'] for township in townships}
    commitments_by_township = {township['ts_pcode']: 0 for township in townships}

    commitments_by_township_natural = {}
    for township in commitments_by_township:
        commitments_by_township_natural[township] = commitments_by_township[township]
        commitments_by_township_natural[township + '_natural'] = 0

    commitments_by_township = commitments_by_township_natural

    activity_queryset = list(activity_queryset)
    locations = aims.TransactionValueLocation.objects.filter(activity__in=activity_queryset).filter(activity__activity_status__code=2, transaction__transaction_type='C').exclude(location__adm_country_adm1__contains="Nation-wide").exclude(location__adm_country_adm2=None).values('pk','location__adm_country_adm2').annotate(dollars=Sum('dollars'))
    for location in locations:
        try:
            commitments_by_township[township_dict[location['location__adm_country_adm2'].lower()]] = base_utils.prettify_compact(location['dollars'])
            commitments_by_township[township_dict[location['location__adm_country_adm2'].lower()] + '_natural'] = location['dollars']
        except KeyError:
            pass

    commitments_by_township = unicode(commitments_by_township).replace("u'", "'")

    return commitments_by_township


def total_donors(activity_queryset):
    '''
    aid_by: donor
    '''

    activity_queryset = list(activity_queryset)
    total_donors = aims.organisation.objects.select_related('activity')\
                                            .filter(activity_participating_organisation__role="Funding")\
                                            .filter(activity__in=activity_queryset)\
                                            .values().distinct().count()
    return total_donors


def total_donors_by_type(activity_queryset=None):
    '''
    aid_by: donor
    '''
    if activity_queryset is None:
        activity_queryset = aims.activity.objects.all()

    activity_queryset = list(activity_queryset)
    total_donors_by_type = aims.organisation_type.objects.filter(organisation__activity_participating_organisation__activity__in=activity_queryset,
                                                                 organisation__activity_participating_organisation__role="Funding")\
                                            .values('code', 'name').annotate(value=Count('organisation'))

    total_donors_by_type = unicode(total_donors_by_type).replace(" u'", " '")

    return total_donors_by_type


def commitment_by_status(activity_queryset=None):
    '''
    aid_by: location (duplicate)
    '''
    if activity_queryset is None:
        activity_queryset = aims.activity.objects.all()

    activity_queryset = list(activity_queryset)
    commitment_by_status = aims.activity_status.objects.filter(activity__in=activity_queryset,\
                                                        activity__transaction__transaction_type="C")\
                                                        .values('name', 'code')\
                                                        .annotate(value=Sum('activity__transaction__value_in__dollars'))

    commitment_by_status = [{'code': status['code'],
                           'name': status['name'],
                           'value': status['value'] or 0,
                           'pretty': base_utils.prettify_compact(status['value'] or 0)}\
                            for status in commitment_by_status]

    commitment_by_status = unicode(commitment_by_status).replace(" u'", " '")

    return commitment_by_status


def loans_vs_grants(transaction_queryset=None):
    '''
    aid_by: donor
    '''
    if transaction_queryset is None:
        transaction_queryset = aims.transaction.objects

    total_transactions = transaction_queryset.filter(transaction_type="C").count()
    loans = transaction_queryset.filter(transaction_type="C", finance_type__code__startswith="4").count()
    grants = total_transactions - loans

    loans_vs_grants = [
         {'name': "Loans", 'code':6, 'value': loans},
         {'name': "Grants", 'code':3, 'value': grants}
         ]

    return loans_vs_grants


def detail_activity(activity, transaction_queryset=None, current_organisation=None):

    if transaction_queryset is None:
        transaction_queryset = aims.transaction.objects

    transaction_activity = transaction_queryset.filter(activity=activity)

    total_spent = total_disbursements(transaction_activity)
    total_planned = total_commitments(transaction_activity)

    location_activity = [location.adm_country_adm1 if location.adm_country_adm2 is ''
                            else location.adm_country_adm2 for location in activity.location_set.all()]

    implementing_partner = [partner.organisation.name for partner in \
                                        activity.activity_participating_organisation_set.filter(role="Implementing").exclude(organisation=None)]

    roles = []
    if current_organisation is not None:
        roles = [participating_organisation.role.name.lower() for participating_organisation in 
                    activity.activity_participating_organisation_set.filter(organisation=current_organisation)]
        if activity.reporting_organisation.pk == current_organisation.pk:
            roles.append('reporting')

    activity_detail = {
                            'object': activity,
                            'spent': base_utils.prettify_compact(total_spent),
                            'percent': percent_disbursed(total_planned, total_spent),
                            'location': location_activity,
                            'partners': implementing_partner,
                            'budget': base_utils.prettify_compact(activity.total_budget),
                            'roles': roles
                        }

    return activity_detail


def activity_statuses_total(activity_queryset=None, organisation=None, json=True):

    if activity_queryset is None:
        activity_queryset = aims.activity.objects.all()

    activities = {status.code: {
        'name': status.name,
        'code': status.name.lower().replace('', ''),
        'value': 0,
        'activities': 0,
        'pretty': base_utils.prettify_compact(0)}
        for status in aims.activity_status.objects.all()}

    activity_queryset = list(activity_queryset)
    activity_statuses = aims.activity_status.objects.filter(activity__in=activity_queryset,
                                                            activity__transaction__transaction_type="C",
                                                            activity__transaction__provider_organisation=organisation)\
                                                    .values('name', 'code')\
                                                    .annotate(value=Count('activity'),
                                                            total=Sum('activity__transaction__value_in__dollars'))

    for status in activity_statuses:
        try:
            code = status['code']
            activities[code]['value'] = float(status['total']) or 0
            activities[code]['activities'] = status['value']
            activities[code]['pretty'] = base_utils.prettify_compact(status['total'] or 0)
        except:
            pass

    activities = activities.values()

    if json:
        activities = unicode(activities).replace(" u'", " '")

    return activities


def percentage_by_status(activity_queryset=None, organisation=False, json=True):

    if activity_queryset is None:
        activity_queryset = aims.activity.objects.all()

    activity_statuses = activity_statuses_total(activity_queryset, organisation, False)

    total = 0
    for status in activity_statuses:
        total += status['value']

    for status in activity_statuses:
        status['value'] = ((status['value'] * 100) / total) if total > 0 else 0
        status['pretty'] = '%s - %.2f%%' % (status['pretty'], status['value'])

    if json:
        activity_statuses = unicode(activity_statuses).replace(" u'", " '")

    return activity_statuses


def transactions_by_year(activity_queryset=None, organisation=None, activity_statuses=[2, ], json=True):

    if not activity_queryset:
        activity_queryset = aims.activity.objects.all()

    activity_queryset = list(activity_queryset)
    transactions_queryset = aims.transaction.objects.filter(activity__activity_status__code__in=activity_statuses,
                                                            provider_organisation=organisation)\
                                                    .order_by('transaction_date')

    transactions_year = []
    for transaction in transactions_queryset:
        if transaction.transaction_date and transaction.transaction_date.year not in transactions_year:
            transactions_year.append(transaction.transaction_date.year)

    transactions_by_year = []

    types_totals = {
        'C': 0,
        'D': 0,
        'E': 0,
        'O': 0
    }

    label_types = {
        'C': 'Commitments',
        'D': 'Disbursements',
        'E': 'Expenditures',
        'O': 'Others',
    }

    for transaction_year in transactions_year:

        totals_transactions = transactions_queryset.filter(transaction_date__year=transaction_year)\
            .values('transaction_type_id').annotate(total=Sum('value_in__dollars'))

        current_year_totals = types_totals.copy()
        for totals in totals_transactions:
            if totals['transaction_type_id'] in current_year_totals:
                current_year_totals[totals['transaction_type_id']] += (totals['total'] or 0)
            else:
                current_year_totals['O'] += (totals['total'] or 0)

        for key, value in current_year_totals.items():
            label = label_types[key]
            current_year_totals[label] = value
            current_year_totals[label + '_Pretty'] = base_utils.prettify_compact(value)

        current_year_totals['year'] = transaction_year

        transactions_by_year.append(current_year_totals)

    if json:
        transactions_by_year = unicode(transactions_by_year).replace(" u'", " '")

    return transactions_by_year


def commitment_disbursement_by_month_year(activity_queryset=None, json=True):

    if not activity_queryset:
        activity_queryset = aims.activity.objects.all()

    activity_queryset = list(activity_queryset)
    transactions_queryset = aims.transaction.objects.filter(activity__in=activity_queryset,transaction_type__in=["C","D"])\
                                                    .order_by( 'transaction_date' )

    first_date = None
    last_date = None
    if transactions_queryset:
        first_date = transactions_queryset.first().transaction_date
        last_date = transactions_queryset.last().transaction_date

    #month_delta = datetime.timedelta(days=30)

    last_commitment = 0
    last_disbursement = 0
    transactions_by_month_year = []

    if first_date and last_date:

        first_date = datetime.date(first_date.year, first_date.month, 1 )
        last_date = datetime.date(last_date.year, last_date.month, 1 )

        while first_date <= last_date:
            total_commitments = transactions_queryset.filter(transaction_date__year=first_date.year, transaction_date__month=first_date.month,
                                                    transaction_type_id='C')\
                                                    .aggregate(total=Sum('value_in__dollars'))

            total_disbursements = transactions_queryset.filter(transaction_date__year=first_date.year, transaction_date__month=first_date.month,
                                                    transaction_type_id='D')\
                                                    .aggregate(total=Sum('value_in__dollars'))

            if total_commitments['total'] or total_disbursements['total']:

                last_commitment += ( total_commitments['total'] or 0 )
                last_disbursement += ( total_disbursements['total'] or 0 )

                transactions_by_month_year.append(
                    {
                        'month_year': first_date.strftime('%m/%Y'),
                        'Commitments': last_commitment or 0,
                        'Commitments_Pretty': base_utils.prettify_compact(last_commitment or 0),
                        'Disbursements': last_disbursement or 0,
                        'Disbursements_Pretty': base_utils.prettify_compact(last_disbursement or 0)
                    }
                )

            first_date = base_utils.add_months( first_date, 1)

    if json:
        transactions_by_month_year = unicode(transactions_by_month_year).replace(" u'", " '")

    return transactions_by_month_year


