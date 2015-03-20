import datetime
import calendar

from django.utils.translation import ugettext_lazy as _
from datetime import timedelta

UNKNOWN_CATEGORY_CODE = '000'
UNKNOWN_CATEGORY_NAME = _("Unknown")
UNKNOWN_SECTOR_NAME = _("Unknown")
UNKNOWN_CONTACT_NAME = _("Unknown")
UNKNOWN_PERCENTAGE = _("?")

UNKNOWN_DONOR_CODE = '000'
UNKNOWN_DONOR_NAME = _("Unnamed")


def prettify(decimal_number):
    if decimal_number >= 1000000000000:
        return decimal_number / 1000000000000, _("trillion")
    if decimal_number >= 1000000000:
        return decimal_number / 1000000000, _("billion")
    if decimal_number >= 1000000:
        return decimal_number / 1000000, _("million")
    if decimal_number >= 1000:
        return decimal_number / 1000, _("thousand")
    return decimal_number, ""


def prettify_compact(decimal_number):
    if decimal_number is None : decimal_number = 0;
    if decimal_number >= 1000000000000:
        decimal_number /= 1000000000000
        unit_marker = "T"
    elif decimal_number >= 1000000000:
        decimal_number /= 1000000000
        unit_marker = "B"
    elif decimal_number >= 1000000:
        decimal_number /= 1000000
        unit_marker = "M"
    elif decimal_number >= 1000:
        decimal_number /= 1000
        unit_marker = "K"
    else:
        unit_marker = ""
    return "%(value).2f%(unit_marker)s" % {'value': decimal_number, 'unit_marker': unit_marker}


def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=(date.month + 1), day=1) - timedelta(days=1)


def last_day_of_last_month(date):
    return date.replace(month=date.month, day=1) - timedelta(days=1)


def arrange_category_info_row(category, value, activity_count=None):
    name = UNKNOWN_DONOR_NAME
    category_code = UNKNOWN_DONOR_CODE

    if category is not None:
        category_code = category.code
        if category.name is not None:
            name = category.name
        else:
            name = category_code
    return [name, value, category_code, prettify_compact(value), activity_count]


def arrange_donor_info_row(donor, value, activity_count=None):
    name = UNKNOWN_DONOR_NAME
    long_name = name
    donor_code = UNKNOWN_DONOR_CODE

    if donor is not None:
        donor_code = donor.code
        if donor.name is not None:
            long_name = donor.name
        elif donor.abbreviation is not None:
            long_name = donor.abbreviation
        else:
            long_name = donor.code
        if donor.abbreviation is not None:
            name = donor.abbreviation
        elif donor.name is not None:
            name = donor.name
        else:
            name = donor_code
    return [name, value, donor_code, long_name, prettify_compact(value), activity_count]

def add_months(sourcedate, months ):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min( sourcedate.day,calendar.monthrange(year,month)[1] )
    return datetime.date(year,month,day)

def check_editor_privilege(user, organisation):
    editor = False
    if user.is_staff:
        editor = True
    elif hasattr(user, 'userorganisation') and organisation:
        if user.userorganisation.organisations.filter(pk=organisation.pk).exists():
            editor = True
    return editor
