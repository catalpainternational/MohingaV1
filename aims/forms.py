from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from haystack.forms import SearchForm
from crispy_forms import helper
from django_select2 import fields

from geodata.models import country
from IATI import models as IATI
from aims import models
from myanmar import models as myanmar
from decorators import parsleyfy


class FormHelper(helper.FormHelper):

    def __init__(self, *args, **kwargs):
        super(FormHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.form_class = 'form-horizontal'
        self.label_class = 'col-lg-3 col-md-3'
        self.field_class = 'col-lg-8 col-md-8'


#@parsleyfy
class DowncastModelForm(forms.ModelForm):

    remote_data = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        abstract = True
        exclude = ('date_created', 'date_modified')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('auto_id', '%s')
        kwargs.setdefault('label_suffix', '')
        super(DowncastModelForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({
                    'help_text': field.help_text
                })

    def save(self, *args, **kwargs):
        #instance = super(DowncastModelForm, self).save(commit=False)
        if hasattr(self.instance, 'activity_id'):
            if self.instance.activity.id == u'':
                self.instance.activity.id = self.cleaned_data['activity_id']
            if self.instance.activity_id == u'':
                self.instance.activity_id = self.cleaned_data['activity_id']

        if not self.instance.pk:
            self.instance = super(DowncastModelForm, self).save()

        if not hasattr(self.instance, 'remote_data'):
            #local_instance = self._meta.model(remote_data_id=instance.pk)
            local_instance = self.instance.__class__.local_data.related.model(remote_data_id=self.instance.pk)
            local_instance.pk = self.instance.pk
            local_instance.__dict__.update(self.instance.__dict__)
            self.instance = local_instance

        self.instance.save()

        return self.instance


class TitleForm(DowncastModelForm):
    language = forms.ModelChoiceField(queryset=models.language.objects, widget=forms.HiddenInput())

    class Meta:
        help_texts = {
                'title': _("The title of the activity is the name of the activity. This is preferably the formal name of the activity, but does not have to be. The title needs to be complete with any abbreviations or acronyms spelled out."),
            }


class DescriptionForm(DowncastModelForm):
    language = forms.ModelChoiceField(queryset=models.language.objects, widget=forms.HiddenInput())
    type = forms.ModelChoiceField(queryset=models.description_type.objects, widget=forms.HiddenInput(), initial=1)

    class Meta:
        help_texts = {
                'description': _("The description of the activity is a descriptive text, longer than the title, explaining what the activity is. Sometimes it is just a short sentence but could also be more detailed."),
            }


class ObjectivesForm(DowncastModelForm):
    language = forms.ModelChoiceField(queryset=models.language.objects, widget=forms.HiddenInput())
    type = forms.ModelChoiceField(queryset=models.description_type.objects, widget=forms.HiddenInput(), initial=2)

    class Meta:
        help_texts = {
                'description': _("The objectives or purposes of the activity are those that the activity intends to achieve. The objectives need to include a detailed description of the activity and expected outcomes."),
            }


class TargetGroupsForm(DowncastModelForm):
    language = forms.ModelChoiceField(queryset=models.language.objects, widget=forms.HiddenInput())
    type = forms.ModelChoiceField(queryset=models.description_type.objects, widget=forms.HiddenInput(), initial=3)

    class Meta:
        help_texts = {
                'description': _("Target groups describe the groups/entities that will be directly positively affected by the activity. This section may also be used to describe organisations/persons who will benefit from the activity in the long term."),
            }


class ParticipatingOrganisationForm(DowncastModelForm):
    role = forms.ModelChoiceField(queryset=models.organisation_role.objects.exclude(name="Accountable"), help_text=_("Extending: The government entity or development partner agency receiving funds from financing partner(s) for channeling to implementing partner(s). Implementing: The implementer of the activity is the organisation(s) which is/are principally responsible for delivering this activity. Also known as the executing agency, this is the intermediary between the extending agency and the ultimate beneficiary. It can be a private firm, a non-governmental organisation, an educational institution, an association, an institute, a government Ministry, or any other individual or organisation selected to implement the activity. Funding:  organisations contributing financing to the activity"))
    organisation = fields.ModelSelect2Field(required=True, queryset=models.organisation.objects, help_text=_("Development partners extending or implementing funds to achieve activity objectives."))

    class Meta:
        help_texts = {
                'percentage': _("#"),
            }

    def save(self, *args, **kwargs):
        
        if self.instance.pk and not self.instance.organisation:
            self.instance.delete()
        else:
            self.instance = super(ParticipatingOrganisationForm, self).save()

        return self.instance


class MinistryForm(DowncastModelForm):
    role = forms.ModelChoiceField(queryset=models.organisation_role.objects, widget=forms.HiddenInput(), initial="Accountable")
    organisation = fields.ModelSelect2Field(required=False, queryset=models.organisation.objects.filter(code__startswith="MM-FERD"), help_text=_("Government Ministries who are partnering with development partners but not necessarily implementing the activity directly."))

    class Meta:
        help_texts = {
                'percentage': _("Extending: The government entity or development partner agency receiving funds from financing partner(s) for channeling to implementing partner(s). Implementing: The implementer of the activity is the organisation(s) which is/are principally responsible for delivering this activity. Also known as the executing agency, this is the intermediary between the extending agency and the ultimate beneficiary. It can be a private firm, a non-governmental organisation, an educational institution, an association, an institute, a government Ministry, or any other individual or organisation selected to implement the activity."),
            }

    def save(self, *args, **kwargs):
        
        if self.instance.pk and not self.instance.organisation:
            self.instance.delete()
        else:
            self.instance = super(MinistryForm, self).save()

        return self.instance


class FinancingForm(DowncastModelForm):
    role = forms.ModelChoiceField(queryset=models.organisation_role.objects, widget=forms.HiddenInput(), initial="Funding")
    organisation = fields.ModelSelect2Field(required=False, queryset=models.organisation.objects, help_text=_("All organisations contributing financing to the activity."))

    class Meta:
        help_texts = {
                'percentage': _("#"),
            }


class ActivitySectorForm(DowncastModelForm):
    sector = fields.ModelSelect2Field(queryset=models.sector.objects.exclude(code__startswith=550), help_text=_("The sectors of the activity explain whether this is, for example, a health or education project. It does not count if it is just mentioned incidentally within the title, description, etc. It needs to be stated separately and explicitly. If projects are presented by sector on an organisation's website, it must be clearly stated whether the organisation works only in those sectors that are listed."), required=False)
    vocabulary = forms.ModelChoiceField(queryset=models.vocabulary.objects, widget=forms.HiddenInput(), initial="DAC")  # Reporting Organiation

    class Meta:
        fields = ('sector', 'percentage', 'vocabulary')
        parsley_extras = {
            'percentage': {
                'trigger': "change keyup",
                'pattern': "^[0-9]+(\.[0-9]{1,2})?$"
            }
        }

        help_texts = {
                'percentage': _("The percentage breakdown for each sector/sub-sector."),
            }


class ActivityNationalSectorForm(DowncastModelForm):
    sector = fields.ModelSelect2Field(queryset=models.sector.objects.filter(code__startswith=550), help_text=_("The sectors of the activity explain whether this is, for example, a health or education activity. The use of specific sub-sectors is strongly encouraged."), required=False)
    vocabulary = forms.ModelChoiceField(queryset=models.vocabulary.objects, widget=forms.HiddenInput(), initial="RO")  # Reporting Organiation

    class Meta:
        fields = ('sector', 'percentage', 'vocabulary')
        parsley_extras = {
            'percentage': {
                'trigger': "change keyup",
                'pattern': "^[0-9]+(\.[0-9]{1,2})?$"
            }
        }

        help_texts = {
                'percentage': _("The sectors of the activity explain whether this is, for example, a health or education activity. The use of specific sub-sectors is strongly encouraged."),
            }


class LocationForm(DowncastModelForm):
    try:
        COUNTRY = country.objects.get(name="Myanmar")
        nation = [('', '---------'), (COUNTRY.pk, COUNTRY.name + ' (Nationwide)'), ]

        states = [(place.pk, place) for place in myanmar.State.objects.all().order_by('st')]
        townships = [(place.pk, place) for place in myanmar.Township.objects.all().order_by('st')]
        places = nation + states + townships
    except:
        nation = [('', '---------'), ]
        places = ()

    place = fields.Select2ChoiceField(choices=places, required=False, help_text="A geographical location within which the activity is taking place within Myanmar. National-level activities can be labelled Myanmar.")

    class Meta:
        fields = ('place', 'percentage')
        parsley_extras = {
            'percentage': {
                'trigger': "change keyup",
                'pattern': "^[0-9]+(\.[0-9]{1,2})?$"
            }
        }

        help_texts = {
                'percentage': _("The percentage of the activity taking place in this location."),
            }

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        if self.instance.gazetteer_entry:
            COUNTRY = country.objects.get(name="Myanmar")

            if self.instance.gazetteer_entry == COUNTRY.pk:
                self.fields['place'].initial = COUNTRY.pk
            else:
                place = myanmar.State.objects.filter(st_pcode=self.instance.gazetteer_entry)
                if len(place) != 0:
                    self.fields['place'].initial = place[0].pk
                else:
                    self.fields['place'].initial = myanmar.Township.objects.get(ts_pcode=self.instance.gazetteer_entry).pk

    def save(self, *args, **kwargs):
        COUNTRY = country.objects.get(name="Myanmar")

        instance = super(LocationForm, self).save(commit=False)
        place_pk = self.cleaned_data['place']

        if place_pk != COUNTRY.pk:
            place = myanmar.State.objects.filter(id=place_pk)
            if len(place) != 0:
                place = place[0]
            else:
                place = myanmar.Township.objects.get(id=place_pk)
        else:
            place = COUNTRY
            instance.gazetteer_entry = COUNTRY.pk

        instance.name = unicode(place)
        instance.adm_country_iso = COUNTRY
        instance.adm_country_name = instance.adm_country_iso.name
        instance.gazetteer_ref = models.gazetteer_agency.objects.all().first()

        if place.__class__ == myanmar.Township:
            instance.adm_country_adm1 = place.st
            instance.adm_country_adm2 = place.ts
            instance.gazetteer_entry = place.ts_pcode

        if place.__class__ == myanmar.State:
            instance.adm_country_adm1 = place.st
            instance.gazetteer_entry = place.st_pcode

        instance.save()
        return instance


class ResultForm(DowncastModelForm):
    class Meta:
        help_texts = {
                'result_type': _("A measurable result of aid work."),
                'title': _("A short, human-readable title."),
                'description': _('A longer, human-readable description.'''),
            }


class ContactForm(DowncastModelForm):
    class Meta:
        parsley_extras = {
             'email': {
                 'trigger': "change keyup",
                 'type': "email",

             }
         }

        help_texts = {
                'person_name': _("The name of the contact person at the organisation."),
                'organisation': _("The organisation to contact for more information about the activity."),
                'telephone': _('The contact telephone number, if available.'''),
                'email': _("The contact email address, if available."),
                'mailing_address': _("The contact mailing address, if available."),
            }

TitleFormset = inlineformset_factory(models.activity, IATI.title, form=TitleForm, can_delete=False, extra=2, max_num=2)
DescriptionFormset = inlineformset_factory(models.activity, IATI.description, form=DescriptionForm, exclude=('rsr_description_type_id', ), can_delete=False, extra=2, max_num=2)

ActivitySectorFormset = inlineformset_factory(models.activity, IATI.activity_sector, form=ActivitySectorForm, can_delete=True, extra=10)
ActivityNationalSectorFormset = inlineformset_factory(models.activity, IATI.activity_sector, form=ActivityNationalSectorForm, can_delete=True, extra=10)

ObjectivesFormset = inlineformset_factory(models.activity, IATI.description, form=ObjectivesForm, exclude=('rsr_description_type_id', ), can_delete=False, max_num=2, extra=2)
TargetGroupsFormset = inlineformset_factory(models.activity, IATI.description, form=TargetGroupsForm, exclude=('rsr_description_type_id', ), can_delete=False, max_num=2, extra=2)
ResultFormset = inlineformset_factory(models.activity, IATI.result, form=ResultForm, can_delete=False, extra=1, max_num=3)

FinancingFormset = inlineformset_factory(models.activity, IATI.activity_participating_organisation, form=FinancingForm, exclude=('name', 'date_created', 'date_modified'), can_delete=False, max_num=10, extra=10)
MinistryFormset = inlineformset_factory(models.activity, IATI.activity_participating_organisation, form=MinistryForm, exclude=('name', 'date_created', 'date_modified'), can_delete=True, max_num=10, extra=10)
ParticipatingOrganisationFormset = inlineformset_factory(models.activity, IATI.activity_participating_organisation, form=ParticipatingOrganisationForm, exclude=('name', 'date_created', 'date_modified'), can_delete=True, max_num=15, extra=15)

LocationFormset = inlineformset_factory(models.activity, IATI.location, form=LocationForm, can_delete=True, max_num=14, extra=14)

ContactFormset = inlineformset_factory(models.activity, IATI.contact_info, form=ContactForm, can_delete=False, max_num=1)


@parsleyfy
#class ActivityForm(DowncastModelForm):
class ActivityForm(forms.ModelForm):
    hierarchy_choices = (
        (1, _("Project")),
        (2, _("Program")),
        )

    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    remote_data = forms.CharField(widget=forms.HiddenInput(), required=False)
    is_draft = forms.BooleanField(widget=forms.HiddenInput(), required=False, initial=False)
    reporting_organisation = fields.ModelSelect2Field(queryset=models.organisation.objects, required=True, help_text=_("The organisation reporting on the activity. This could be a development partner reporting on activities being financed/implemented directly, or an extending partner reporting on behalf of implementing partners."))
    hierarchy = forms.ChoiceField(choices=hierarchy_choices, required=False, help_text=_("Identifies whether the activity is part of a broader programme or standalone."))
    policy_marker = fields.ModelSelect2MultipleField(queryset=models.policy_marker.objects, required=False, help_text=_("Policy Markers help monitor aid targeting key environmental, gender and other policy objectives. Multiple markers can be selected if needed."))
    collaboration_type = forms.ModelChoiceField(queryset=models.collaboration_type.objects, required=False, help_text=_("The type of collaboration involved in the project's disbursements, e.g. bilateral or multilateral. The collaboration type shows how the activity is funded - whether directly from one government to another (bilaterally), through institutions such as the World Bank or UN (multilaterally), or otherwise."))
    #participating_organisation = fields.ModelSelect2MultipleField(label=_("Sector Working Groups"), queryset=models.organisation.objects.filter(code__icontains="MM-FERD-SWG"), required=False, help_text=_("Identifies which Myanmar Sector Working Group this activity falls within. Multiple Sector Working Groups can be identified if the activity is cross-sectoral in nature."))
    start_planned = forms.CharField(widget=forms.DateInput(attrs={'class': 'input-date'}), required=False, help_text=_("The planned start date and end dates of the activity. If there are one set of dates but they are not explicitly stated as planned or actual dates, it is assumed that they are planned dates."))
    end_planned = forms.CharField(widget=forms.DateInput(attrs={'class': 'input-date'}), required=False, help_text=_("The planned start date and end dates of the activity. If there are one set of dates but they are not explicitly stated as planned or actual dates, it is assumed that they are planned dates."))
    start_actual = forms.CharField(widget=forms.DateInput(attrs={'class': 'input-date'}), required=False, help_text=_("The actual start date reflects the commencement of funding or the date the project/programme agreement is signed."))
    end_actual = forms.CharField(widget=forms.DateInput(attrs={'class': 'input-date'}), required=False, help_text=_("The actual end date reflects, wherever possible, the ending of physical activity."))

    class Meta:
        model = models.activity
        fields = ('id', 'iati_identifier', 'reporting_organisation', 'hierarchy', 'policy_marker', 'activity_status', 'start_planned', 'end_planned',
                  'start_actual', 'end_actual', 'collaboration_type', 'default_flow_type', 'default_aid_type',
                  'default_finance_type', 'default_tied_status', 'total_budget_currency', 'total_budget')
        parsley_extras = {
            'total_budget': {
                'trigger': "change keyup",
                'pattern': "^[0-9]+(\.[0-9]{1,2})?$",
                }
            }

        help_texts = {
                'iati_identifier': _("A globally unique identifier for the activity. This should be in the form of the IATI Organisation Identifier (for the reporting organisation) concatenated to that organisation activity identifier."),
                'activity_status': _("This shows whether the activity is currently being planned/negotiated or under design (pipeline/identification), being implemented (implementation), has finished (completed), has been cancelled (cancelled) or has undergone a final post-completion review/evaulation (post-completion)."),
                'default_flow_type': _("The type of assistance provided, e.g. Official Development Assistance (ODA)."),
                'default_aid_type': _("The type of aid being supplied (budget support, debt relief, etc.). This element specifies a default for all the activity's financial transactions. This can be overridden at the individual transaction level."),
                'default_finance_type': _("The type of finance shows whether the activity is a grant, loan, export credit or otherwise. This is the default value for all the activities transactions. This can be overridden by individual transactions."),
                'default_tied_status': _("Specify whether the aid is untied, tied, or partially tied. Tied aid could be where procurement is restricted to the donor organisation/country whereas untied aid is where more open procurement is used."),
                'total_budget_currency': _("The default ISO 4217 currency code for all financial values related to this activity. This can be overridden at the individual transaction level."),
                'total_budget': _("This refers to the total financial commitment for the activity as a whole for the lifetime of the activity. This is a high level commitment rather than a detailed breakdown of the activity budget. Total estimated commitment is accepted."),
            }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('auto_id', '%s')
        kwargs.setdefault('label_suffix', '')
        super(ActivityForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({
                    'help_text': field.help_text
                })

        self.fields['iati_identifier'].widget.attrs['readonly'] = True
        self.fields['activity_status'].required = True
        self.fields['total_budget'].label = _("Total planned budget")

    def save(self, *args, **kwargs):
        instance = super(self.__class__, self).save(commit=False)
        if not hasattr(instance, 'remote_data'):
            local_instance = self._meta.model(remote_data_id=instance.pk)
            local_instance.pk = instance.pk
            local_instance.__dict__.update(self.instance.__dict__)
            instance = local_instance

        if hasattr(instance, 'is_draft'):
            instance.is_draft = self.cleaned_data['is_draft']

        # clean dates replacing empty strings with None to avoid validity error
        for date in ['start_planned', 'end_planned', 'start_actual', 'end_actual']:
            if not instance.__dict__[date]:
                instance.__dict__[date] = None

        instance.save()

        COUNTRY = country.objects.get(name="Myanmar")
        if COUNTRY not in instance.recipient_country.all():
            recipient_country = models.activity_recipient_country(activity=instance, country=COUNTRY)
            recipient_country.save()

        # Set the Total Budget Currency to the Default Currency
        instance.default_currency = instance.total_budget_currency
        instance.save()

        return instance

    def clean(self):
        cleaned_data = super(ActivityForm, self).clean()

        start_planned = cleaned_data.get("start_planned")
        end_planned = cleaned_data.get("end_planned")

        if start_planned and end_planned and start_planned > end_planned:
            message = _('Started planned date can not be later than End planned date')
            self._errors["start_planned"] = self.error_class([message])
            raise forms.ValidationError(message)

        start_actual = cleaned_data.get("start_actual")
        end_actual = cleaned_data.get("end_actual")

        if start_actual and end_actual and start_actual > end_actual:
            message = _('Started actual date can not be later than End actual date')
            self._errors["start_actual"] = self.error_class([message])
            raise forms.ValidationError(message)

        return cleaned_data


class OrganisationForm(DowncastModelForm):
    code = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = models.organisation
        fields = ('name', 'abbreviation', 'type')


class TransactionForm(DowncastModelForm):
    activity = forms.ModelChoiceField(models.activity.objects.with_drafts(), widget=forms.HiddenInput())
    provider_organisation = fields.ModelSelect2Field(queryset=models.organisation.objects.all())
    receiver_organisation = fields.ModelSelect2Field(queryset=models.organisation.objects.all(),  required=False)
    transaction_date = forms.CharField(widget=forms.DateInput(attrs={'class': 'input-date'}))
    value_date = forms.CharField(widget=forms.DateInput(attrs={'class': 'input-date'}))

    class Meta:
        model = models.transaction
        exclude = ('remote_data', 'ref', 'provider_activity', 'date_created', 'date_modified',
                 'description_type', 'provider_organisation_name', 'receiver_organisation_name', 'is_draft')
        parsley_extras = {
            'activity': {
                'required': "false"
            },
            'value': {
                'trigger': "change keyup",
                'pattern': "^-?[0-9]+(\.[0-9]{1,2})?$",
            }
        }

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.instance.description_type = models.description_type.objects.get(code=1)
        self.fields['transaction_type'].required = True
        self.fields['currency'].required = True


class ActivitySearchForm(SearchForm):
    q = forms.CharField(label="", max_length=128, required=False)

    reporting_organisation = forms.ModelChoiceField(models.organisation.objects, required=False)
    sector = forms.ModelChoiceField(models.sector.objects, required=False)
    participating_organisation = forms.ModelChoiceField(models.organisation.objects, required=False)

    def __init__(self, *args, **kwargs):
        super(ActivitySearchForm, self).__init__(*args, **kwargs)
        self.fields['q'].widget.attrs['class'] = "form-control"
        self.fields['reporting_organisation'].widget.attrs['class'] = "form-control"
        self.fields['sector'].widget.attrs['class'] = "form-control"
        self.fields['participating_organisation'].widget.attrs['class'] = "form-control"

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        search_queryset = super(ActivitySearchForm, self).search()
        if not self.is_valid():
            return self.no_query_found()

        # Check to see if a organisation was chosen.
        if self.cleaned_data['reporting_organisation']:
            search_queryset = search_queryset.filter(reporting_organisation=self.cleaned_data['reporting_organisation'])

        # Check to see if an sector was chosen.
        if self.cleaned_data['sector']:
            search_queryset = search_queryset.filter(sectors__contains=self.cleaned_data['sector'].code)

        if self.cleaned_data['participating_organisation']:
            search_queryset = search_queryset.filter(participating_organisations__contains=self.cleaned_data['participating_organisation'].name)

        return search_queryset.order_by('-django_ct')
