import json
import datetime
import urllib

from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, View
from django.views.generic.edit import UpdateView, CreateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.core.serializers import serialize
from django.db import transaction

from aims import models as aims
from aims import forms as aims_forms
from aims import charts
from aims import base_utils
from profiles import models as profiles_models
from profiles import forms as profiles_forms
from myanmar.models import State


class OrganisationProfile(TemplateView):
    template_name = "profiles/donor.html"

    def get_context_data(self, **kwargs):
        context = super(OrganisationProfile, self).get_context_data(**kwargs)

        donor_code = self.kwargs['iati_identifier'] if 'iati_identifier' in kwargs else '0'

        organisation = get_object_or_404(
            aims.organisation.objects, code=urllib.unquote(donor_code))
        organisation_profile, created = profiles_models.OrganisationProfile.objects.get_or_create(
            organisation=organisation)

        contact, created = profiles_models.Contact.objects.get_or_create(
            organisation_profile=organisation_profile)

        people = profiles_models.Person.objects.filter(
            organisation_profile=organisation_profile).order_by('order')

        contact_form = profiles_forms.ContactForm(instance=contact)
        person_form = profiles_forms.PersonForm(
            initial={'organisation_profile': organisation_profile})

        # Editor permissions
        editor = base_utils.check_editor_privilege(self.request.user, organisation)

        activities = aims.activity.aims.with_drafts() if editor else aims.activity.aims.all()
        activities_by_role = activities.filter(activity_participating_organisation__organisation=organisation)\
            .distinct()

        transaction_queryset = aims.transaction.objects.filter(provider_organisation=organisation)

        try:
            first_statistics = transaction_queryset.order_by('transaction_date')[0].transaction_date.year
        except:
            first_statistics = datetime.datetime.now().year

        activity_statuses = aims.activity_status.objects.all()
        organisation_roles = aims.organisation_role.objects.exclude(code='Accountable')

        total_commitments = charts.total_commitments(transaction_queryset, None, activity_statuses)
        total_disbursements = charts.total_disbursements(transaction_queryset, activity_statuses)
        executed = charts.percent_disbursed(total_commitments, total_disbursements)

        total_spent_current_year = charts.total_disbursements(
            transaction_queryset.filter(transaction_date__year=datetime.datetime.now().year), activity_statuses)

        commitment_by_category = charts.commitment_by_category(transaction_queryset, None, 20, activity_statuses, False)

        donor_information = base_utils.arrange_donor_info_row(organisation, 0)

        activities_organisation = [charts.detail_activity(activity, current_organisation=organisation)
                                   for activity in activities_by_role]

        activities_statuses = charts.activity_statuses_total(activities_by_role, organisation)
        percentage_statuses = charts.percentage_by_status(activities_by_role, organisation)
        transactions_by_year = charts.transactions_by_year(activities_by_role, organisation, activity_statuses)

        activities_reporting = activities.filter(reporting_organisation=organisation)\
            .exclude(id__in=activities_by_role).distinct()

        activities_reporting = [charts.detail_activity(activity, current_organisation=organisation)
                                for activity in activities_reporting]
        activities_organisation = activities_organisation + activities_reporting

        user = self.request.user
        for key, activity in enumerate(activities_organisation):
            reporting_organisation = activity['object'].reporting_organisation
            activities_organisation[key]['editor'] = base_utils.check_editor_privilege(user, reporting_organisation)

        context['contact'] = contact
        context['activities'] = activities_by_role
        context['first_statistics_year'] = first_statistics
        context['activities_organisation'] = activities_organisation
        context['total_commitments'] = base_utils.prettify_compact(total_commitments)
        context['total_spent_current_year'] = base_utils.prettify_compact(total_spent_current_year)
        context['total_disbursements'] = base_utils.prettify_compact(total_disbursements)
        context['commitment_by_category'] = commitment_by_category
        context['activity_by_status'] = activities_statuses
        context['percentage_statuses'] = percentage_statuses
        context['transactions_by_year'] = transactions_by_year
        context['executed'] = executed
        context['contact_form'] = contact_form
        context['person_form'] = person_form
        context['form_helper'] = aims_forms.FormHelper()
        context['people'] = people
        context['organisation_profile'] = organisation_profile
        context['organisation'] = organisation
        context['activity_statuses'] = activity_statuses
        context['organisation_roles'] = organisation_roles
        context['token'] = self.request.META.get('CSRF_COOKIE', None)
        context['current_donor'] = {
            'name': donor_information[3],
            'code': donor_information[2]
        }

        context['editor'] = editor
        for person in context['people']:
            person.editor = editor

        return context


class ActivityProfile(TemplateView):
    template_name = "profiles/activity.html"

    def get_context_data(self, **kwargs):
        context = super(ActivityProfile, self).get_context_data(**kwargs)

        try:
            iati_identifier = urllib.unquote(self.kwargs['iati_identifier'])
            activity = aims.activity.aims.with_drafts().get(iati_identifier=iati_identifier)

            user = self.request.user
            if activity.is_draft and not user.is_staff:
                if not user.userorganisation.organisations.filter(pk=activity.reporting_organisation.pk).exists():
                    raise Exception(_('Activity is defined as draft'))
        except:
            raise Http404(_('Activity not found'))

        activity_sector = activity.sectors.order_by('-percentage')

        funding_organisations = activity.activity_participating_organisation_set.filter(
            role__code='Funding')

        participating_organisations = activity.activity_participating_organisation_set.filter(
            role__code__in=['Extending', 'Implementing'])

        ministry_organisations = activity.activity_participating_organisation_set.filter(
            role__code='Accountable')

        general_description = activity.description_set.filter(type__code=1).first()
        objective_description = activity.description_set.filter(type__code=2).first()
        target_group_description = activity.description_set.filter(type__code=3).first()

        locations = charts.commitments_percentage_by_state(activity, False)

        activity_status_code = activity.activity_status.code if activity.activity_status else None

        total_commitments = charts.total_commitments(activity.transaction_set, None, [activity_status_code])
        total_disbursements = charts.total_disbursements(activity.transaction_set, [activity_status_code])

        percent_disbursed = charts.percent_disbursed(total_commitments, total_disbursements)

        commitment_disbursement_by_month_year = charts.commitment_disbursement_by_month_year([activity])

        states_queryset = State.objects
        context['commitments_by_location'] = charts.commitments_by_state([activity], states_queryset)
        context['json_borders'] = "mm_states.json"

        context['activity'] = activity
        context['activity_sector'] = activity_sector

        context['funding_organisations'] = funding_organisations
        context['participating_organisations'] = participating_organisations
        context['ministry_organisations'] = ministry_organisations

        context['general_description'] = general_description
        context['objective_description'] = objective_description
        context['target_group_description'] = target_group_description

        context['locations'] = locations

        context['total_budget'] = base_utils.prettify_compact(activity.total_budget)

        try:
            if activity.total_budget:
                budget = activity.total_budget_in.dollars
            else:
                budget = 0
        except:
            budget = 0

        context['total_budget_dollars'] = base_utils.prettify_compact(budget)
        context['percent_disbursed'] = percent_disbursed
        context['commitment_disbursement_by_month_year'] = commitment_disbursement_by_month_year
        context['transaction_queryset'] = activity.transaction_set.all()

        return context


class AjaxableResponseMixin(object):

    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response


class SaveContact(AjaxableResponseMixin, UpdateView):
    form_class = profiles_forms.ContactForm
    model = profiles_models.Contact

    def get_success_url(self):
        return "/profile/donor/%s/" % self.object.organisation_profile.organisation.code


class CreatePerson(AjaxableResponseMixin, CreateView):
    template_name = "profiles/donor.html"
    form_class = profiles_forms.PersonForm
    model = profiles_models.Person

    def get_success_url(self):
        return "/profile/donor/%s/" % self.object.organisation_profile.organisation.code


class UpdatePerson(AjaxableResponseMixin, UpdateView):
    template_name = "profiles/donor.html"
    form_class = profiles_forms.PersonForm
    model = profiles_models.Person

    def get_success_url(self):
        return "/profile/donor/%s/" % self.object.organisation_profile.organisation.code


class PersonView(TemplateView):
    template_name = 'profiles/person.html'

    def get(self, *args, **kwargs):
        person = get_object_or_404(profiles_models.Person, pk=kwargs['pk'])
        context = super(PersonView, self).get_context_data()

        organisation = person.organisation_profile.organisation

        editor = True if self.request.user.is_authenticated()\
            and (self.request.user.is_staff or
                 self.request.user.userorganisation.organisations.filter(pk=organisation.pk))\
            else False
        person.editor = editor

        context['person'] = person

        return self.render_to_response(context)


class ContactView(TemplateView):
    template_name = 'profiles/contact.html'

    def get(self, *args, **kwargs):
        contact = get_object_or_404(profiles_models.Contact, pk=kwargs['pk'])
        context = super(ContactView, self).get_context_data()
        context['contact'] = contact

        return self.render_to_response(context)


class PersonData(View):

    def get(self, *args, **kwargs):

        person = get_object_or_404(profiles_models.Person, pk=kwargs['pk'])

        json = serialize('json', [person])
        json = json.strip("[]")

        return HttpResponse(json, mimetype="application/json")


class DeletePerson(View):

    def get(self, *args, **kwargs):

        person = profiles_models.Person.objects.get(pk=kwargs['pk'])
        data = {}
        try:
            person.delete()
            data['status'] = 1
        except Exception:
            data['status'] = 0

        return HttpResponse(json.dumps(data), content_type="application/json")


class ReorderPeople(View):

    def get(self, *args, **kwargs):

        people = self.request.GET.getlist('people[]')

        with transaction.commit_on_success():
            for idx, person in enumerate(people):
                person_object = get_object_or_404(profiles_models.Person, pk=person)
                person_object.order = idx
                person_object.save()

        return HttpResponse('{success:true}', mimetype="application/json")


class UpdateGeneric(View):

    def boolify(self, s):
        if s == 'True' or s == 'true':
            return True
        if s == 'False' or s == 'false':
            return False
        if s == 'None' or s == 'none':
            return None
        raise ValueError('Not Boolean Value!')

    def automatic_cast(self, var):
        var = str(var)
        for caster in (self.boolify, int, float):
            try:
                return caster(var)
            except ValueError:
                pass
        return var

    def post(self, *args, **kwargs):

        class_name = self.request.POST['class']
        pk = self.request.POST['pk']
        field_name = self.request.POST['name']

        try:
            field_value = self.request.POST['value']
            if not field_value:
                field_value = None
        except Exception:
            field_value = self.request.POST.getlist('value[]')

        if 'cast' in self.request.POST.keys():
            field_value = self.automatic_cast(field_value)

        cls = profiles_models.__dict__[class_name]
        instance = cls.objects.get(pk=pk)

        if type(field_value) == list:
            attr = getattr(instance, field_name)
            attr.clear()
            for i in field_value:
                attr.add(i)
        else:
            setattr(instance, field_name, field_value)
            instance.save()

        return HttpResponse()


class UploadGeneric(View):

    def post(self, *args, **kwargs):

        class_name = self.request.POST['class']
        pk = self.request.POST['pk']
        field_name = self.request.POST['name']

        form = profiles_forms.ImageUploadForm(self.request.POST, self.request.FILES)
        if form.is_valid():

            cls = profiles_models.__dict__[class_name]
            instance = cls.objects.get(pk=pk)

            setattr(instance, field_name, form.cleaned_data['image'])
            instance.save()
            instance.resize_image(field_name)

            data = {'image': getattr(instance, field_name).url}
            return HttpResponse(json.dumps(data), mimetype="application/json")
