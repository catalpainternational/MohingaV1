from datetime import date

from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

from caching.base import CachingManager, CachingMixin

from IATI import models as IATI


ORIGINAL_TYPE = 'original'
PENDING_TYPE = 'pending'
DIFFERENCE_TYPES = (
        (ORIGINAL_TYPE, _("original")),
        (PENDING_TYPE, _("pending")),
    )


class AIMSManager(models.Manager):

    def get_queryset(self,):
        queryset = super(AIMSManager, self).get_queryset()
        try:
            return queryset.exclude(is_draft=True)
        except:
            return queryset

    def with_drafts(self,):
        return super(AIMSManager, self).get_queryset()

    def drafts(self,):
        queryset = super(AIMSManager, self).get_queryset()
        try:
            return queryset.filter(is_draft=True)
        except:
            return queryset.none()


class CurrencyQuerySet(QuerySet):

    def closest_to(self, rate_date):
        closest_greater_qs = self.filter(date__gt=rate_date).order_by('date')
        closest_less_qs = self.filter(date__lt=rate_date).order_by('-date')

        try:
            try:
                closest_greater = closest_greater_qs[0]
            except IndexError:
                return closest_less_qs[0]

            try:
                closest_less = closest_less_qs[0]
            except IndexError:
                return closest_greater_qs[0]
        except IndexError:
            raise self.model.DoesNotExist("There is no closest object"
                                          " because there are no objects.")

        if closest_greater.date - rate_date > rate_date - closest_less.date:
            return closest_less
        else:
            return closest_greater


class CurrencyManager(CachingManager):

    def get_query_set(self):
        return CurrencyQuerySet(self.model, using=self._db)

    def closest_to(self, rate_date):
        return self.get_query_set().closest_to(rate_date)


class CurrencyExchangeRate(CachingMixin, models.Model):
    base_currency = models.ForeignKey(IATI.currency, verbose_name=_("Base Currency"), related_name='base_currencies')
    currency = models.ForeignKey(IATI.currency, verbose_name=_("Exchange Currency"), related_name="exchange_currencies")
    rate = models.DecimalField(verbose_name=_("Exchange Rate"), decimal_places=8, max_digits=16)
    date = models.DateField()

    objects = CurrencyManager()

    class Meta:
        db_table = 'aims_currency_exchange_rate'

    def __unicode__(self,):
        return "%s -> %s : %s" % (self.base_currency.code, self.currency.code, self.rate)


class ActivityTotalBudgetUSD(models.Model):
    activity = models.OneToOneField(IATI.activity, verbose_name="Activity Budget in USD", related_name="total_budget_in")
    rate = models.ForeignKey(CurrencyExchangeRate, null=True, blank=True)
    dollars = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'aims_activity_total_budget_usd'

    def __unicode__(self,):
        return "%s USD$%s" % (self.activity, self.dollars)


class TransactionValueUSD(models.Model):
    transaction = models.OneToOneField(IATI.transaction, verbose_name="Transaction Value in USD", related_name="value_in")
    rate = models.ForeignKey(CurrencyExchangeRate, null=True, blank=True)
    dollars = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'aims_transaction_value_usd'

    def __unicode__(self,):
        return "%s USD$%s" % (self.transaction, self.dollars)


class TransactionValueLocation(models.Model):
    activity = models.ForeignKey(IATI.activity, related_name='transaction_value_for_location', null=True, blank=True)
    transaction = models.ForeignKey(IATI.transaction, related_name='transaction_value_for_location', null=True, blank=True)
    location = models.ForeignKey(IATI.location, related_name='transaction_value_for_location', null=True, blank=True)
    currency = models.ForeignKey(IATI.currency, null=True, blank=True)
    value = models.FloatField(null=True, blank=True)
    dollars = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'aims_transaction_value_location'


class UserOrganisation(models.Model):
    user = models.OneToOneField(User)
    organisations = models.ManyToManyField(IATI.organisation, related_name='users', null=True, blank=True)

    def __unicode__(self,):
        return self.user


class Difference(models.Model):
    difference_type = models.CharField(choices=DIFFERENCE_TYPES, max_length=64)
    field_name = models.CharField(max_length=200)
    field_value = models.CharField(max_length=600, null=True, blank=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=200)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return u"%s - %s - %s - %s" % (self.content_object, self.difference_type, self.field_name, self.field_value)


class LocalDataMixin(CachingMixin, models.Model):
    differences = generic.GenericRelation('Difference')

    date_created = models.DateField(verbose_name=_('Date Created'), null=True, blank=True)
    date_modified = models.DateField(verbose_name=_('Last Modified'), null=True, blank=True)

    # objects = CachingManager()
    objects = AIMSManager()
    aims = AIMSManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        previous_self = self.__class__.objects.filter(pk=self.pk)
        super(LocalDataMixin, self).save(*args, **kwargs)

        if len(previous_self) != 0:
            previous_self = previous_self[0]
            diffs = [(key, previous_self.__dict__[key]) for key in previous_self.__dict__.keys() if not key.startswith('_') and previous_self.__dict__[key] != self.__dict__[key]]
            for diff in diffs:
                try:
                    difference = self.differences.get(field_name=diff[0], difference_type=ORIGINAL_TYPE)
                    difference.field_value = diff[1]
                except:
                    difference = Difference(content_object=self, field_name=diff[0], field_value=diff[1], difference_type=ORIGINAL_TYPE)
                difference.save()


### IATI derived models

class activity_date_type(LocalDataMixin, IATI.activity_date_type):

    remote_data = models.OneToOneField(IATI.activity_date_type, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class activity_status(LocalDataMixin, IATI.activity_status):

    remote_data = models.OneToOneField(IATI.activity_status, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class aid_type_category(LocalDataMixin, IATI.aid_type_category):

    remote_data = models.OneToOneField(IATI.aid_type_category, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class aid_type(LocalDataMixin, IATI.aid_type):

    remote_data = models.OneToOneField(IATI.aid_type, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class budget_type(LocalDataMixin, IATI.budget_type):

    remote_data = models.OneToOneField(IATI.budget_type, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class collaboration_type(LocalDataMixin, IATI.collaboration_type):

    remote_data = models.OneToOneField(IATI.collaboration_type, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class condition_type(LocalDataMixin, IATI.condition_type):

    remote_data = models.OneToOneField(IATI.condition_type, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class currency(LocalDataMixin, IATI.currency):

    remote_data = models.OneToOneField(IATI.currency, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class description_type(LocalDataMixin, IATI.description_type):

    remote_data = models.OneToOneField(IATI.description_type, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class disbursement_channel(LocalDataMixin, IATI.disbursement_channel):

    remote_data = models.OneToOneField(IATI.disbursement_channel, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class document_category(LocalDataMixin, IATI.document_category):

    remote_data = models.OneToOneField(IATI.document_category, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class file_format(LocalDataMixin, IATI.file_format):

    remote_data = models.OneToOneField(IATI.file_format, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class finance_type_category(LocalDataMixin, IATI.finance_type_category):

    remote_data = models.OneToOneField(IATI.finance_type_category, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class finance_type(LocalDataMixin, IATI.finance_type):

    remote_data = models.OneToOneField(IATI.finance_type, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class flow_type(LocalDataMixin, IATI.flow_type):

    remote_data = models.OneToOneField(IATI.flow_type, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class gazetteer_agency(LocalDataMixin, IATI.gazetteer_agency):

    remote_data = models.OneToOneField(IATI.gazetteer_agency, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class geographical_precision(LocalDataMixin, IATI.geographical_precision):

    remote_data = models.OneToOneField(IATI.geographical_precision, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class indicator_measure(LocalDataMixin, IATI.indicator_measure):

    remote_data = models.OneToOneField(IATI.indicator_measure, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class language(LocalDataMixin, IATI.language):

    remote_data = models.OneToOneField(IATI.language, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class location_type(LocalDataMixin, IATI.location_type):

    remote_data = models.OneToOneField(IATI.location_type, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class organisation_identifier(LocalDataMixin, IATI.organisation_identifier):

    remote_data = models.OneToOneField(IATI.organisation_identifier, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class organisation_role(LocalDataMixin, IATI.organisation_role):

    remote_data = models.OneToOneField(IATI.organisation_role, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class organisation_type(LocalDataMixin, IATI.organisation_type):

    remote_data = models.OneToOneField(IATI.organisation_type, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class policy_marker(LocalDataMixin, IATI.policy_marker):

    remote_data = models.OneToOneField(IATI.policy_marker, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class policy_significance(LocalDataMixin, IATI.policy_significance):

    remote_data = models.OneToOneField(IATI.policy_significance, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class publisher_type(LocalDataMixin, IATI.publisher_type):

    remote_data = models.OneToOneField(IATI.publisher_type, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class related_activity_type(LocalDataMixin, IATI.related_activity_type):

    remote_data = models.OneToOneField(IATI.related_activity_type, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class result_type(LocalDataMixin, IATI.result_type):

    remote_data = models.OneToOneField(IATI.result_type, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class sector(LocalDataMixin, IATI.sector):

    remote_data = models.OneToOneField(IATI.sector, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class sector_category(LocalDataMixin, IATI.sector_category):

    remote_data = models.OneToOneField(IATI.sector_category, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class tied_status(LocalDataMixin, IATI.tied_status):

    remote_data = models.OneToOneField(IATI.tied_status, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class transaction_type(LocalDataMixin, IATI.transaction_type):

    remote_data = models.OneToOneField(IATI.transaction_type, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class value_type(LocalDataMixin, IATI.value_type):

    remote_data = models.OneToOneField(IATI.value_type, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class verification_status(LocalDataMixin, IATI.verification_status):

    remote_data = models.OneToOneField(IATI.verification_status, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class vocabulary(LocalDataMixin, IATI.vocabulary):

    remote_data = models.OneToOneField(IATI.vocabulary, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class organisation(LocalDataMixin, IATI.organisation):

    remote_data = models.OneToOneField(IATI.organisation, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class activity(LocalDataMixin, IATI.activity):

    is_draft = models.BooleanField(default=False)
    remote_data = models.OneToOneField(IATI.activity, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")

    @property
    def title(self,):

        current_language = get_language()
        title_object = self.title_set.filter(language__code=current_language).first()

        try:
            if title_object and title_object.title:
                title = title_object.title
            else:
                title_object = self.title_set.exclude(title=None).first()
                title = title_object.title  
        except:
            title = ''

        return title

    def _get_description(self, type):

        current_language = get_language()
        description_object = self.description_set.filter(type__code=type, language__code=current_language).first()

        try:
            if description_object and description_object.description:
                description = description_object.description
            else:
                description_object = self.description_set.exclude(description=None).first()
                description = description_object.title

        except:
            description = ''

        return description

    @property
    def general_description(self,):
        return self._get_description(1)

    @property
    def objective_description(self,):
        return self._get_description(2)

    @property
    def target_group_description(self,):
        return self._get_description(3)

    @property
    def sectors(self):
        return self.activity_sector_set.exclude(vocabulary__code='RO')

    @property
    def national_sectors(self):
        return self.activity_sector_set.filter(vocabulary__code='RO')

    def save(self, *args, **kwargs):
        super(activity, self).save(*args, **kwargs)
        transaction.aims.with_drafts().filter(activity=self).update(is_draft=self.is_draft)

class activity_participating_organisation(LocalDataMixin, IATI.activity_participating_organisation):

    remote_data = models.OneToOneField(IATI.activity_participating_organisation, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")

    def save(self, *args, **kwargs):
        if self.organisation:
            self.name = self.organisation.name
        super(activity_participating_organisation, self).save(*args, **kwargs)


class activity_policy_marker(LocalDataMixin, IATI.activity_policy_marker):

    remote_data = models.OneToOneField(IATI.activity_policy_marker, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class activity_sector(LocalDataMixin, IATI.activity_sector):

    remote_data = models.OneToOneField(IATI.activity_sector, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class activity_recipient_country(LocalDataMixin, IATI.activity_recipient_country):

    remote_data = models.OneToOneField(IATI.activity_recipient_country, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class activity_recipient_region(LocalDataMixin, IATI.activity_recipient_region):

    remote_data = models.OneToOneField(IATI.activity_recipient_region, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class other_identifier(LocalDataMixin, IATI.other_identifier):

    remote_data = models.OneToOneField(IATI.other_identifier, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class activity_website(LocalDataMixin, IATI.activity_website):

    remote_data = models.OneToOneField(IATI.activity_website, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class contact_info(LocalDataMixin, IATI.contact_info):

    remote_data = models.OneToOneField(IATI.contact_info, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class transaction(LocalDataMixin, IATI.transaction):

    is_draft = models.BooleanField(default=False)
    remote_data = models.OneToOneField(IATI.transaction, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")

    def save(self, *args, **kwargs):
        transaction_activity = activity.objects.with_drafts().filter(remote_data=self.activity)
        if transaction_activity.count() > 0:
            self.is_draft = transaction_activity.first().is_draft
        super(transaction, self).save(*args, **kwargs)


# class transaction_description(LocalDataMixin, IATI.transaction_description):
#
#    # iati_data = models.OneToOneField(IATI.transaction_description, verbose_name=_("IATI Data"), parent_link=True, related_name="aims_data")


class planned_disbursement(LocalDataMixin, IATI.planned_disbursement):

    remote_data = models.OneToOneField(IATI.planned_disbursement, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class related_activity(LocalDataMixin, IATI.related_activity):

    remote_data = models.OneToOneField(IATI.related_activity, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class document_link(LocalDataMixin, IATI.document_link):

    remote_data = models.OneToOneField(IATI.document_link, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class result(LocalDataMixin, IATI.result):

    remote_data = models.OneToOneField(IATI.result, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class title(LocalDataMixin, IATI.title):

    remote_data = models.OneToOneField(IATI.title, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class description(LocalDataMixin, IATI.description):

    remote_data = models.OneToOneField(IATI.description, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class budget(LocalDataMixin, IATI.budget):

    remote_data = models.OneToOneField(IATI.budget, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class condition(LocalDataMixin, IATI.condition):

    remote_data = models.OneToOneField(IATI.condition, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


class location(LocalDataMixin, IATI.location):

    remote_data = models.OneToOneField(IATI.location, verbose_name=_("Remote Data"), parent_link=True, related_name="local_data")


def import_missing_iati_data():

    iati_app = models.get_app('IATI')
    aims_app = models.get_app('aims')

    aims_models = models.get_models(aims_app)
    for iati_model in models.get_models(iati_app):
        for aims_model in aims_models:
            if issubclass(aims_model, iati_model):
                rowset = iati_model.objects.all()
                for row in rowset:
                    try:
                        if row.pk and not aims_model.objects.with_drafts().filter(remote_data_id=row.pk).exists():
                            new_row = aims_model()
                            new_row.pk = row.pk
                            new_row.__dict__.update(row.__dict__)
                            new_row.date_created = timezone.now()
                            new_row.save()

                    except Exception as e:
                        print e
                        return
