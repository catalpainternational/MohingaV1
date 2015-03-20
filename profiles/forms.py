from django import forms
from django.utils.translation import ugettext_lazy as _

from parsley.decorators import parsleyfy

from profiles import models


@parsleyfy
class ContactForm(forms.ModelForm):

    class Meta:
        model = models.Contact
        widgets = {
            'organisation_profile': forms.HiddenInput(),
            'address': forms.Textarea(attrs={'rows': 3})
        }
        parsley_extras = {
             'email': {
                 'trigger': "change keyup",
                 'type': "email",

             }
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields.get('title').required = True
        self.fields.get('address').required = True


@parsleyfy
class PersonForm(forms.ModelForm):

    class Meta:
        model = models.Person
        widgets = {
            'organisation_profile': forms.HiddenInput(),
            'background': forms.Textarea(attrs={'rows': 3})
        }
        parsley_extras = {
             'email': {
                 'trigger': "change keyup",
                 'type': "email",

             },
        }

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)

        self.fields['background'].label = _("Brief biography (limit 500 characters)")

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({
                    'placeholder': field.label,
                    'class': 'form-control'
                })
                field.label = ''

        self.fields.get('name').required = True


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
