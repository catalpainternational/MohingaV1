from django import template
from django.utils.translation import ugettext as _

register = template.Library()


@register.filter()
def to_date(value):
    if value:
        value = value.strftime('%Y%m%d')
        return value


@register.filter()
def date_format(value):
    if value:
        value = value.strftime('%Y-%m-%d')
        return value


@register.filter()
def to_int(value):
    values = filter(str.isdigit, str(value))
    if values:
        return values


@register.filter
def financing_organisation(activity):

    financing_organisation_name = ''
    financing_organisation = activity.transaction_set.values_list('provider_organisation__name', flat=True).distinct()

    if len(financing_organisation) > 1:
        financing_organisation_name = _('Multiple Donors')
    elif len(financing_organisation) > 0:
        financing_organisation_name = financing_organisation[0]

    return financing_organisation_name
