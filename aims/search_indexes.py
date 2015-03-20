from haystack import indexes

from IATI import models as IATI
from aims import models as aims
# from geodata import models as geodata


class TestIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    reporting_organisation = indexes.CharField(model_attr='reporting_organisation', null=True)
    participating_organisations = indexes.CharField(model_attr='participating_organisation', null=True)
    sectors = indexes.CharField(model_attr='sector', null=True)

    def prepare_sectors(self, obj):
        return [sector.pk for sector in obj.sector.all()]

    def prepare_participating_organisations(self, obj):
        return [org.name for org in obj.participating_organisation.all()]

    def get_model(self):
        return aims.activity

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().aims.all()


class OrganisationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    code = indexes.CharField(model_attr='code', null=True)
    name = indexes.CharField(model_attr='name', null=True)
    abbreviation = indexes.CharField(model_attr='abbreviation', null=True)

    def get_model(self):
        return aims.organisation

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
