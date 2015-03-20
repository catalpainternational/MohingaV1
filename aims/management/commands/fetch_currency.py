from django.core.management.base import BaseCommand

import requests

from aims import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        rates = requests.get("http://openexchangerates.org/api/currencies.json").json()
        for code in rates:
            currency, created = models.currency.objects.get_or_create(code=code)
            if created:
                currency.name = rates[code]
                currency.save()
            # print code, rates[code]
