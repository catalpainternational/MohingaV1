from __future__ import unicode_literals
from datetime import date
from decimal import Decimal

from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from aims import models as aims
from IATI import models as IATI

from haystack.signals import BaseSignalProcessor
from haystack.exceptions import NotHandled


class RealtimeSignalProcessor(BaseSignalProcessor):
    """
    Allows for observing when saves/deletes fire & automatically updates the
    search engine appropriately.
    """
    def setup(self):
        # Naive (listen to all model saves).
        models.signals.post_save.connect(self.handle_save)
        models.signals.post_delete.connect(self.handle_delete)
        # Efficient would be going through all backends & collecting all models
        # being used, then hooking up signals only for those.

    def teardown(self):
        # Naive (listen to all model saves).
        models.signals.post_save.disconnect(self.handle_save)
        models.signals.post_delete.disconnect(self.handle_delete)
        # Efficient would be going through all backends & collecting all models
        # being used, then disconnecting signals only for those.

    def handle_save(self, sender, instance, **kwargs):
        """
        Given an individual model instance, determine which backends the
        update should be sent to & update the object on those backends.
        """
        using_backends = self.connection_router.for_write(instance=instance)

        for using in using_backends:

            # if hasattr(instance, 'remote_data'):
            #     original_class = instance.__class__
            #     sender = instance.__class__ = instance.remote_data.__class__

            try:
                index = self.connections[using].get_unified_index().get_index(sender)
                index.update_object(instance, using=using)
                # if hasattr(instance, 'remote_data'):
                #     instance.__class__ = original_class
            except:
                pass
                # if hasattr(instance, 'remote_data'):
                #     instance.__class__ = original_class


@receiver(post_save)
def save_total_budget_in_dollars(sender, instance, **kwargs):
    if sender not in [IATI.activity, aims.activity]:
        return

    # exit out when laoding fixtures
    if kwargs['raw']:
        return

    if not instance.iati_identifier:
        instance.iati_identifier = instance.id
        instance.save()

    if instance.total_budget_currency:
        if instance.total_budget and instance.total_budget_currency.code != "USD":
            rate_date = instance.start_planned or instance.start_actual or date.today()
            currency_rate = aims.CurrencyExchangeRate.objects.filter(base_currency=instance.total_budget_currency, currency__code="USD").closest_to(rate_date)
            total_budget_in_dollars = instance.total_budget * currency_rate.rate
        else:
            currency_rate = None
            total_budget_in_dollars = instance.total_budget

        total_budget, created = aims.ActivityTotalBudgetUSD.objects.get_or_create(activity=instance)
        total_budget.rate = currency_rate
        total_budget.dollars = total_budget_in_dollars
        total_budget.save()

    if instance.total_budget:
        for location in instance.location_set.all():
            for transaction in instance.transaction_set.all():
                percentage = location.percentage if location.percentage else 100.0

                transaction_value_location, created = aims.TransactionValueLocation.objects.get_or_create(transaction=transaction, activity=instance, location=location)
                transaction_value_location.value = instance.total_budget * Decimal(percentage) * Decimal(0.01)
                transaction_value_location.currency = instance.default_currency
                transaction_value_location.dollars = transaction.value_in.dollars * float(percentage) * 0.01
                transaction_value_location.save()


@receiver(post_save)
def save_transaction_value_in_dollars(sender, instance, **kwargs):
    if sender not in [IATI.transaction, aims.transaction]:
        return

    if instance.currency:
        if instance.currency.code != "USD":
            rate_date = instance.transaction_date or instance.value_date or date.today()
            currency_rate = aims.CurrencyExchangeRate.objects.filter(base_currency=instance.currency, currency__code="USD").closest_to(rate_date)
            value_in_dollars = instance.value * currency_rate.rate
        else:
            currency_rate = None
            value_in_dollars = instance.value

        transaction_value, created = aims.TransactionValueUSD.objects.get_or_create(transaction=instance)
        transaction_value.rate = currency_rate
        transaction_value.dollars = value_in_dollars
        transaction_value.save()

    # get the locations from the activity
    # per each location's percentage create / set the transaction_value_location values
    # if a location has been removed from the activity the transaction value location should also be deleted

    if instance.value:
        for location in instance.activity.location_set.all():
            percentage = location.percentage if location.percentage else Decimal(100)

            transaction_value_location, created = aims.TransactionValueLocation.objects.get_or_create(transaction=instance, activity=instance.activity, location=location)
            transaction_value_location.value = instance.value * percentage * Decimal(.01)
            transaction_value_location.currency = instance.currency
            transaction_value_location.dollars = value_in_dollars * percentage * Decimal(.01)
            transaction_value_location.save()


@receiver(post_save)
def save_iati_data_in_aims(sender, instance, **kwargs):

    if len(sender.__subclasses__()) > 0:
        for subclass in sender.__subclasses__():
            if hasattr(subclass, 'remote_data'):
                if not subclass.objects.with_drafts().filter(remote_data_id=instance.pk).exists():
                    new_row = subclass()
                    new_row.pk = instance.pk
                    new_row.__dict__.update(instance.__dict__)
                    new_row.date_created = timezone.now()
                    new_row.save()
