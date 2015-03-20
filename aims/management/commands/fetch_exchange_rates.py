from datetime import datetime

from django.core.management.base import BaseCommand
from django.conf import settings

from IATI.models import transaction
from geodata.models import country
import requests


from aims import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        #number_of_days = 365 * 2  # fetch exchage rates going back 2 years
        #base = datetime.today()
        #dates = (base - datetime.timedelta(days=x) for x in range(0, number_of_days))
        myanmar = country.objects.get(name="Myanmar")

        dates = transaction.objects.filter(activity__recipient_country=myanmar, activity__activity_status__in=[1, 2]
                           ).order_by('value_date').values_list('value_date').distinct()
        for data in dates:
            date = data[0]
            if date is None:
                continue
            if models.CurrencyExchangeRate.objects.filter(date=date).exists():
                # print "Already have rates for this date:", date.isoformat()
                continue

            request = requests.get("http://openexchangerates.org/api/historical/%s.json?app_id=%s" % (date.strftime('%Y-%m-%d'), settings.OPEN_EXCHANGE_API_KEY))

            if request.status_code == 200:
                exchange = request.json()
                base_currency = models.currency.objects.get(code=exchange['base'])

                for code in exchange['rates']:
                    # print code
                    try:
                        # save the rate
                        currency = models.currency.objects.get(code=code)
                        exchange_rate = models.CurrencyExchangeRate(currency=currency, base_currency=base_currency, rate=exchange['rates'][code])
                        exchange_rate.date = date
                        exchange_rate.save()

                        # save the inverse rate
                        inverse_exchange_rate = models.CurrencyExchangeRate(currency=base_currency, base_currency=currency, rate=(1 / exchange['rates'][code]))
                        inverse_exchange_rate.date = date
                        inverse_exchange_rate.save()

                    except:
                        pass
                        # print "unsupported currency", code, date.isoformat()
