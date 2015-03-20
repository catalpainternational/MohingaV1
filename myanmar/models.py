from django.contrib.gis.db import models


class Country(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=254)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()


country_mapping = {
    'id': 'Id',
    'name': 'Name',
    'geom': 'MULTIPOLYGON',
}


class State(models.Model):
    objectid = models.IntegerField()
    st = models.CharField(max_length=50)
    st_pcode = models.CharField(max_length=6)
    st_mya = models.CharField(max_length=254)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    st_short = models.CharField(max_length=254)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.st


state_mapping = {
    'objectid': 'OBJECTID',
    'st': 'ST',
    'st_pcode': 'ST_PCODE',
    'st_mya': 'ST_MYA',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'st_short': 'ST_SHORT',
    'geom': 'MULTIPOLYGON',
}


class Township(models.Model):
    objectid = models.IntegerField()
    st = models.CharField(max_length=50)
    st_pcode = models.CharField(max_length=6)
    dt = models.CharField(max_length=50)
    dt_pcode = models.CharField(max_length=10)
    ts = models.CharField(max_length=50)
    ts_mya = models.CharField(max_length=50)
    ts_pcode = models.CharField(max_length=9)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    def __unicode__(self):
        return u"%s (%s)" % (self.ts, self.st)


township_mapping = {
    'objectid': 'OBJECTID',
    'st': 'ST',
    'st_pcode': 'ST_PCODE',
    'dt': 'DT',
    'dt_pcode': 'DT_PCODE',
    'ts': 'TS',
    'ts_mya': 'TS_MYA',
    'ts_pcode': 'TS_PCODE',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'geom': 'MULTIPOLYGON',
}
