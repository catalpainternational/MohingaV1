from django.db import models

from PIL import Image, ImageOps

from IATI import models as IATI


class ImageModel(object):

    QUALITY = 100
    image_size = {}

    def thumb_image(self, path, width, height):

        image = Image.open(path)

        image = image.convert("RGBA")

        ImageOps.fit(image, (width, height), Image.ANTIALIAS).save(path, quality=self.QUALITY)

    def resize_image(self, image):

        if image not in self.image_size:
            return False

        image_property = getattr(self, image)
        size = self.image_size[image]

        self.thumb_image(image_property.path, size[0], size[1])


class OrganisationProfile(models.Model, ImageModel):

    image_size = {
        'logo': [200, 200],
        'banner_image': [1500, 350]
    }

    organisation = models.ForeignKey(IATI.organisation, related_name='profile')

    url = models.URLField(null=True, blank=True)
    background = models.TextField(max_length=2400, null=True, blank=True)
    logo = models.ImageField(upload_to="profiles/organisation_logo/", null=True, blank=True)
    banner_image = models.ImageField(upload_to="profiles/organisation_banner_image/", null=True, blank=True)
    banner_text = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self,):
        return self.organisation.name


class Contact(models.Model):
    organisation_profile = models.ForeignKey(OrganisationProfile, related_name="contacts", null=True, blank=True)
    title = models.CharField(max_length=64, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    phone_number = models.CharField(max_length=64, null=True, blank=True)
    email = models.CharField(max_length=128, null=True, blank=True)
    fax = models.CharField(max_length=128, null=True, blank=True)

    def __unicode__(self,):
        return self.organisation_profile.organisation.name


class Person(models.Model, ImageModel):

    image_size = {
        'photo': [115, 115]
    }

    organisation_profile = models.ForeignKey(OrganisationProfile, related_name="persons")

    name = models.CharField(max_length=128, null=True, blank=True)
    position = models.CharField(max_length=128, null=True, blank=True)
    background = models.CharField(max_length=500, null=True, blank=True)
    phone_number = models.CharField(max_length=128, null=True, blank=True)
    email = models.CharField(max_length=128, null=True, blank=True)
    photo = models.ImageField(upload_to="profiles/person_photo", null=True, blank=True)
    order = models.IntegerField(blank=True, null=True, default=0)

    def __unicode__(self,):
        return self.name
