import os

from django.contrib.gis.utils import LayerMapping
from django.core.management.base import BaseCommand

from myanmar import models


class Command(BaseCommand):
    """
    load all the shapefile data
    """
    def handle(self, *args, **options):

        country_shp = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                '../../data/1_adm0_country_250k_mimu/adm0_country_250k_mimu.shp'))
        state_shp = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                '../../data/2_adm1_states_regions1_250k_mimu/adm1_states_regions1_250k_mimu.shp'))
        township_shp = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                '../../data/5_adm3_townships1_250k_mimu/adm3_townships1_250k_mimu.shp'))

        country_layer_mapping = LayerMapping(models.Country, country_shp, models.country_mapping,
                          transform=False, encoding='iso-8859-1')
        state_layer_mapping = LayerMapping(models.State, state_shp, models.state_mapping,
                          transform=False, encoding='iso-8859-1')
        township_layer_mapping = LayerMapping(models.Township, township_shp, models.township_mapping,
                          transform=False, encoding='iso-8859-1')

        country_layer_mapping.save(strict=True, verbose=True)
        state_layer_mapping.save(strict=True, verbose=True)
        township_layer_mapping.save(strict=True, verbose=True)
