import os
import re
import random
from datetime import date, datetime
from time import strptime

from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.core.files.temp import NamedTemporaryFile
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
from django.views.generic import View, RedirectView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.db import transaction

from endless_pagination.views import AjaxListView
from haystack.views import SearchView as HayStackSearchView

from geodata.models import country
from aims.models import activity, sector_category, organisation, organisation_role

from aims import base_utils, forms
from aims.exports import export_activities

from aims import models as aims
from aims import charts

from myanmar.models import State, Township


titles = {
    'location': _('Aid By Location'),
    'ministry': _('Aid By Ministry'),
    'sector': _('Aid By Sector'),
    'donor': _('Aid By Donor')}


def aims_sections(subset):
    tmp = [
        {'key': 'location', 'title': _('Aid By Location'), 'url': reverse('aid_by', kwargs={'subset': subset, 'section': 'location'})},
        {'key': 'ministry', 'title': _('Aid By Ministry'), 'url': reverse('aid_by', kwargs={'subset': subset, 'section': 'ministry'})},
        {'key': 'sector', 'title': _('Aid By Sector'), 'url': reverse('aid_by', kwargs={'subset': subset, 'section': 'sector'})},
        {'key': 'donor', 'title': _('Aid By Donor'), 'url': reverse('aid_by', kwargs={'subset': subset, 'section': 'donor'})},
    ]
    aspects = []
    for item in tmp:
        # if item['key'] is not ignore:
        aspects.append(item)
    return aspects


def disable_fields_in_form(form, editor):
    if not editor:
        for key in form.fields.keys():
            form.fields[key].widget.attrs['disabled'] = 'disabled'
    return form


def disable_fields_in_formset(formset, editor):
    if not editor:
        for form in formset:
            for key in form.fields.keys():
                form.fields[key].widget.attrs['disabled'] = 'disabled'
    return formset


class RedirectToDefault(RedirectView):

    permanent = False

    def get_redirect_url(self, **kwargs):
        return reverse('aid_by', kwargs={'subset': 'CPU', 'section': 'location'})


class AidBy(AjaxListView):

    page_template = "aims/activity_page.html"
    template_name = "aims/aid_by.html"
    for_render = False

    #######################################
    # From Endless's views.py, overriding BaseListView
    # site-packages/endless_pagination/views.py l=99
    #######################################
    def get(self, request, *args, **kwargs):
        self.set_subset(**kwargs)
        date_filter_active = self.set_date_range(**kwargs)
        self.set_attributes_from_kwargs(**kwargs)
        self.object_list = self.get_queryset(*args, **kwargs)

        if not self.get_allow_empty() and len(self.object_list) == 0:
            msg = _('Empty list and ``%(class_name)s.allow_empty`` is False.')
            raise Http404(msg % {'class_name': self.__class__.__name__})

        context = self.get_context_data(object_list=self.object_list, page_template=self.page_template)

        if self.is_export():
            object_list = context['object_list']
            if date_filter_active:
                object_list = self.filter_activities_by_daterange(object_list, self.start_date, self.end_date)
            return export_activities(object_list)

        context['date_filter_active'] = date_filter_active

        if request.is_ajax():
            self.template_name = self.page_template

        return self.render_to_response(context)

    def get_queryset(self, *args, **kwargs):
        return aims.activity.objects.all().order_by('-total_budget_in__dollars')

    def filter_activities_by_daterange(self, activity_queryset, start_date, end_date):
        try:
            query = activity_queryset.filter(
                (
                    Q(transaction__isnull=False) &
                    Q(transaction__transaction_date__gte=start_date) &
                    Q(transaction__transaction_date__lte=end_date)
                ) |
                (
                    Q(start_actual__isnull=True) &
                    Q(start_planned__gte=start_date) &
                    Q(start_planned__lte=end_date)
                ) |
                (
                    Q(start_actual__gte=start_date) &
                    Q(start_actual__lte=end_date)
                ) |
                (
                    Q(end_actual__isnull=True) &
                    Q(end_planned__gte=start_date) &
                    Q(end_planned__lte=end_date)
                ) |
                (
                    Q(end_actual__gte=start_date) &
                    Q(end_actual__lte=end_date)
                )
            ).distinct()
        except:
            query = activity_queryset

        return query

    def get_context_data(self, **kwargs):
        context = super(AidBy, self).get_context_data(**kwargs)
        context['subset'] = self.subset
        context['for_render'] = self.for_render
        context['subset_for_render'] = self.subset + "I"
        #start_date = self.start_date or aims.activity.objects.exclude(start_planned=None).order_by('start_planned').first().start_planned
        start_date = self.start_date or date(datetime.now().year - 1, 1, 1)
        end_date = self.end_date or datetime.now()
        context['country'] = self.country
        context['start_date'] = start_date.strftime('%b %Y')
        context['end_date'] = end_date.strftime('%b %Y')
        if hasattr(self.request.user, 'userorganisation'):
            context['userorganisation'] = self.request.user.userorganisation.organisations.first()

        context['object_list'] = self.filter_activities_by_daterange(
            context['object_list'],
            start_date,
            end_date)

        if self.section == 'location':
            context = self.get_location_context(context, state=self.which, **kwargs)
        if self.section == 'sector':
            context = self.get_sector_context(context, start_date, end_date,
                                              category=self.which, sector=self.specific, **kwargs)
        if self.section == 'ministry':
            context = self.get_ministry_context(context, start_date, end_date,
                                                ministry=self.which, **kwargs)
        if self.section == 'donor':
            context = self.get_donor_context(context, start_date, end_date,
                                             donor=self.which, **kwargs)
        context['sections'] = aims_sections(self.subset)
        context['current_section'] = self.section_name
        context['current_title'] = titles[self.section_name]

        for activity_object in context['object_list']:
            activity_object.financing_organisation = activity_object.activity_participating_organisation_set.filter(role="Funding").first()

        return context

    def set_attributes_from_kwargs(self, **kwargs):
        self.country = country.objects.get(name="Myanmar")
        self.subset = kwargs['subset']
        self.section = kwargs['section']

        self.which = kwargs['which'] if 'which' in kwargs else None
        self.specific = kwargs['specific'] if 'specific' in kwargs else None
        self.export = kwargs['export'] if 'export' in kwargs else None

    def set_subset(self, **kwargs):
        # print "Calling set_subset-1", kwargs
        if 'subset' not in kwargs:
            self.subset = "CPU"  # everything
        else:
            self.subset = kwargs['subset']

        if 'I' in self.subset:
            self.subset = self.subset.replace('I', '')
            self.for_render = True

    def set_date_range(self, **kwargs):
        self.start_date, self.end_date = None, None
        if 'date_filter_clear' in self.request.GET:
            self.request.session['start'] = None
            self.request.session['end'] = None
        else:
            if 'start' in self.request.GET:
                self.start_date = self.request.GET['start']
            elif 'start' in self.request.session:
                self.start_date = self.request.session['start']

            if self.start_date:
                try:
                    start_date = strptime(self.start_date, "%b %Y")
                    self.request.session['start'] = self.start_date
                    self.start_date = date(int(start_date.tm_year), int(start_date.tm_mon), 1)
                except:
                    self.start_date = None

            if 'end' in self.request.GET:
                self.end_date = self.request.GET['end']
            elif 'end' in self.request.session:
                self.end_date = self.request.session['end']

            if self.end_date:
                try:
                    end_date = strptime(self.end_date, "%b %Y")
                    self.request.session['end'] = self.end_date
                    self.end_date = date(int(end_date.tm_year), int(end_date.tm_mon), 1)
                    self.end_date = base_utils.last_day_of_month(self.end_date)
                except:
                    self.end_date = None

        if self.start_date or self.end_date:
            return True

    def is_export(self):
        return self.export

    def get_sector_context(self, context, start_date, end_date, category=None, sector=None, **kwargs):

        self.template_name = "aims/aid_by_sector.html"
        self.section_name = 'sector'

        category_code = None

        if category:
            category_code = category
            if category_code != base_utils.UNKNOWN_CATEGORY_CODE:
                category = sector_category.objects.get(code=category_code)
                context['category'] = category
            else:
                context['category'] = {'name': base_utils.UNKNOWN_CATEGORY_NAME, 'code': base_utils.UNKNOWN_CATEGORY_CODE}
            context['filter_name'] = 'category'
            context['filter_value'] = category_code
        if sector:
            context['sector'] = sector_category.objects.get(code=sector)

        # Charts with aggregation and annotation
        context['categories'] = aims.sector_category.objects.all().values_list('name', 'code',).order_by('name')
        # shorten category names
        context['categories'] = [(re.sub(" and ", " & ", cat[0], flags=re.IGNORECASE), cat[1]) for cat in context['categories']]

        # set querysets
        if sector:
            if context['object_list']:
                context['object_list'] = activity_queryset = context['object_list'].filter(activity_sector=sector)
            else:
                context['object_list'] = activity_queryset = aims.activity.objects.all()

            activity_sector_queryset = aims.activity_sector.objects.filter(sector=sector)
        elif category:
            if context['object_list']:
                context['object_list'] = activity_queryset = context['object_list'].filter(activity_sector__sector__code__startswith=category.code)
            else:
                context['object_list'] = activity_queryset = aims.activity.objects.all()
            activity_sector_queryset = aims.activity_sector.objects.filter(sector__code__startswith=category.code)
        else:
            activity_sector_queryset = aims.activity_sector.objects.all()
            if context['object_list']:
                context['object_list'] = activity_queryset = context['object_list']
            else:
                context['object_list'] = activity_queryset = aims.activity.objects.all()

        # early out to avoid getting unnecessary data
        if self.request.is_ajax() or self.is_export():
            return context

        transaction_queryset = aims.transaction.objects.filter(activity__in=activity_queryset)

        total_commitments = charts.total_commitments(transaction_queryset, activity_sector_queryset)
        total_disbursements = charts.total_disbursements(transaction_queryset)
        context['total_commitments'] = base_utils.prettify(total_commitments)
        context['total_disbursements'] = base_utils.prettify(total_disbursements)
        context['executed'] = charts.percent_disbursed(total_commitments, total_disbursements)

        context['activity_statuses'] = charts.activity_statuses(activity_queryset)
        context['donor_commitments'] = charts.donor_commitments(transaction_queryset)
        context['activities_by_ministry'] = charts.activities_by_ministry(activity_queryset)

        transaction_queryset_datefiltered = aims.transaction.objects\
            .filter(activity__in=self.filter_activities_by_daterange(
                aims.activity.objects,
                start_date,
                end_date))

        context['categories_for_horizontal'] = charts.commitment_by_category(transaction_queryset_datefiltered,
                                                                             None,
                                                                             limit=30)

        return context

    def get_location_context(self, context, state=None, specific=None, **kwargs):
        self.template_name = "aims/aid_by_location.html"
        self.section_name = 'location'

        states_queryset = State.objects
        # set all states for select dropdown
        context['states'] = states_queryset.all().values('st_pcode', 'st_short')

        if state:
            # a state is selected in the filter
            state = states_queryset.get(st_pcode=state)
            context['current_state'] = state
            context['st_current'] = state.st_pcode
            context['st_center'] = state.geom.centroid
            context['current_extent'] = state.geom.extent
            context['json_borders'] = "mm_townships.json"
            context['filter_name'] = 'location'
            context['filter_value'] = state.st_pcode

            if context['object_list']:
                context['object_list'] = activity_queryset = context['object_list'].filter(location__adm_country_adm1=state.st)
            else:
                context['object_list'] = activity_queryset = aims.activity.objects.filter(location__adm_country_adm1=state.st)

            township_queryset = Township.objects
            context['commitments_by_location'] = charts.commitments_by_township(activity_queryset, township_queryset)
        else:
            # no state is selected show whole country
            context['json_borders'] = "mm_states.json"

            if context['object_list']:
                context['object_list'] = activity_queryset = context['object_list']
            else:
                context['object_list'] = activity_queryset = aims.activity.objects.all()

            context['commitments_by_location'] = charts.commitments_by_state(activity_queryset.filter(activity_status_id=2),
                                                                                states_queryset)

        # early out to avoid getting unnecessary data
        if self.request.is_ajax() or self.is_export():
            return context

        transaction_queryset = aims.transaction.objects.filter(activity__in=activity_queryset)

        # new style
        context['donor_commitments'] = charts.donor_commitments(transaction_queryset)
        context['donors_count'] = charts.total_donors(activity_queryset)

        total_commitments = charts.total_commitments(transaction_queryset)
        total_disbursements = charts.total_disbursements(transaction_queryset)
        context['total_commitments'] = base_utils.prettify(total_commitments)
        context['total_disbursements'] = base_utils.prettify(total_disbursements)
        context['executed'] = charts.percent_disbursed(total_commitments, total_disbursements)

        context['activities_by_ministry'] = charts.activities_by_ministry(activity_queryset, 4)
        context['activity_statuses'] = charts.activity_statuses(activity_queryset)
        context['commitment_by_category'] = charts.commitment_by_category(transaction_queryset=transaction_queryset, limit=20)
        context['commitment_by_status'] = charts.commitment_by_status(activity_queryset)

        return context

    def get_ministry_context(self, context, start_date, end_date,
                             ministry=None, **kwargs):
        self.template_name = "aims/aid_by_ministry.html"
        self.section_name = "ministry"

        # print "ministry", ministry
        if ministry:
            try:
                current_ministry = organisation.objects.get(code=ministry)
                context['current_ministry'] = current_ministry
                context['filter_name'] = 'ministry'
                context['filter_value'] = current_ministry.code
                if context['object_list']:
                    context['object_list'] = activity_queryset = \
                        context['object_list'].filter(participating_organisation__code=ministry)\
                        .distinct()
                else:
                    context['object_list'] = activity_queryset = aims.activity.objects.all()
            except:
                print "no current ministry found for code", ministry
                pass
        else:
            if not context['object_list']:
                context['object_list'] = activity_queryset = aims.activity.objects.all()
            else:
                activity_queryset = context['object_list']

        # early out to avoid getting unnecessary data
        if self.request.is_ajax() or self.is_export():
            return context

        # new style
        context['ministy_list'] = aims.activity_participating_organisation.objects.exclude(organisation__name=None)\
                                      .filter(role='Accountable')\
                                      .values_list('organisation__code', 'organisation__name')\
                                      .distinct()

        transaction_queryset = aims.transaction.objects.filter(activity__in=activity_queryset)

        context['donor_commitments'] = charts.donor_commitments(transaction_queryset, limit=5)
        context['ministries'] = charts.activities_by_ministry(
            self.filter_activities_by_daterange(aims.activity.objects.all(),
                                                start_date,
                                                end_date),
            limit=None)
        context['total_commitments'] = base_utils.prettify(charts.total_commitments(transaction_queryset))
        context['total_disbursements'] = base_utils.prettify(charts.total_disbursements(transaction_queryset))
        context['total_donors_by_type'] = charts.total_donors_by_type(activity_queryset)

        return context

    def get_donor_context(self, context, start_date, end_date, donor=None, **kwargs):
        self.template_name = "aims/aid_by_donor.html"
        self.section_name = "donor"

        donor_code = None
        if donor:
            donor_code = donor

            if donor_code == base_utils.UNKNOWN_DONOR_CODE:
                context['current_donor'] = {
                    'name': base_utils.UNKNOWN_DONOR_NAME,
                    'code': base_utils.UNKNOWN_DONOR_CODE}
            elif organisation.objects.filter(code=donor_code).exists():
                org = organisation.objects.get(code=donor_code)
                tmp = base_utils.arrange_donor_info_row(org, 0)
                context['current_donor'] = {
                    'name': tmp[3],
                    'code': tmp[2]
                }

            context['filter_name'] = 'donor'
            context['filter_value'] = donor_code

        context['donors'] = aims.transaction.objects.exclude(provider_organisation__name=None)\
                                                    .values_list('provider_organisation__code', 'provider_organisation__name')\
                                                    .distinct()\
                                                    .order_by('provider_organisation__name')
        if context['object_list']:
            if donor:
                if donor == base_utils.UNKNOWN_DONOR_CODE:
                    context['object_list'] = activity_queryset = context['object_list'].filter(transaction__isnull=False, transaction__provider_organisation__isnull=True)
                else:
                    context['object_list'] = activity_queryset = context['object_list'].filter(transaction__provider_organisation__code=donor)
            else:
                activity_queryset = context['object_list']
        else:
            context['object_list'] = activity_queryset = aims.activity.objects.all()

        # early out to avoid getting unnecessary data
        if self.request.is_ajax() or self.is_export():
            return context

        transaction_queryset = aims.transaction.objects.filter(activity__in=activity_queryset)
        transactions_filtered_by_date = aims.transaction.objects\
            .filter(activity__in=self.filter_activities_by_daterange(aims.activity.objects,
                                                                     start_date,
                                                                     end_date))
        if donor:
            if donor == base_utils.UNKNOWN_DONOR_CODE:
                transaction_queryset = transaction_queryset.filter(provider_organisation__isnull=True)
            else:
                transaction_queryset = transaction_queryset.filter(provider_organisation__code=donor)

        if self.start_date and self.end_date:
            transaction_queryset = transaction_queryset.filter(transaction_date__gte=self.start_date,
                transaction_date__lte=self.end_date)

        activity_statuses = aims.activity_status.objects.all()

        total_commitments = charts.total_commitments(transaction_queryset, activity_statuses=activity_statuses)
        total_disbursements = charts.total_disbursements(transaction_queryset, activity_statuses=activity_statuses)

        context['donors_commitments'] = charts.donor_commitments(transactions_filtered_by_date, activity_statuses=activity_statuses)
        context['donors_count'] = charts.total_donors(activity_queryset)
        context['donors_commitment'] = base_utils.prettify(total_commitments)
        context['donors_disbursement'] = base_utils.prettify(total_disbursements)
        context['donors_executed'] = charts.percent_disbursed(total_commitments, total_disbursements)
        context['activities_by_ministry'] = charts.activities_by_ministry(activity_queryset)
        context['activity_statuses'] = charts.activity_statuses(activity_queryset)
        context['loans_vs_grants'] = charts.loans_vs_grants(transaction_queryset)
        context['commitment_by_category'] = charts.commitment_by_category(transaction_queryset=transaction_queryset, limit=30, activity_statuses=activity_statuses)

        return context


class Exporter(View):

    def get(self, request, *args, **kwargs):
        COUNTRY = country.objects.get(name="Myanmar")

        subset = kwargs['subset']
        method = kwargs['method']
        value = None
        name = None
        if 'filter_name' in kwargs:
            name = kwargs['filter_name']
            value = kwargs['filter_value']

        if method == "CSV":
            # print "TODO: filter export by Location and Ministry"
            if name:
                if name == 'donor':
                    activities = utils.relevant_activities(COUNTRY, subset=subset, donor_code=value)
                if name == 'category':
                    activities = utils.relevant_activities(COUNTRY, subset=subset, category_code=value)
                if name == 'ministry':
                    activities = utils.relevant_activities(COUNTRY, subset=subset, ministry_code=value)
                if name == 'location':
                    activities = utils.relevant_activities(COUNTRY, subset=subset, state_code=value)
            else:
                activities = activity.objects.filter(recipient_country=COUNTRY)

            return export_activities(activities)
        elif method == "PNG" or method == "PDF":
            page_name = kwargs['section']
            kwargs = {'subset': subset + "I"}
            page = "aid_by"
            if value:
                kwargs['which'] = value
            kwargs['section'] = page_name

            url = reverse(page, kwargs=kwargs)

            tmp_suffix = "." + page_name + "." + method.lower()
            return_name = page_name + "." + datetime.now().isoformat() + "." + method.lower()
            newfile = NamedTemporaryFile(suffix=tmp_suffix)
            # save your data to newfile.name
            # print "name", return_name
            # print "file", newfile.name
            # print "command", "scraper http://127.0.0.1:8000%s %s" % (url, newfile.name)

            call_command('scraper', settings.SCRAPER_URL + url, newfile.name)

            mime_type = 'application/pdf' if method == "PDF" else 'image/png'

            wrapper = FileWrapper(newfile)
            response = HttpResponse(wrapper, content_type=mime_type)
            response['Content-Disposition'] = 'attachment; filename=%s' % return_name
            response['Content-Length'] = os.path.getsize(newfile.name)
            return response

            # print "python manage.py scraper  http://127.0.0.1:8000%s" % url
        else:
            # print "This export method is not yet supported"
            return None


class CreateLocalActivity(SuccessMessageMixin, CreateView):
    template_name = "aims/edit_data.html"
    form_class = forms.ActivityForm
    model = aims.activity
    success_message = _("Activity was saved successfully")

    def get_success_url(self):
        return "/activity/%s/" % self.object.iati_identifier

    def get_success_message(self, cleaned_data):
        if cleaned_data['is_draft']:
            self.success_message = _("Activity was successfully saved as a draft")
        return self.success_message % cleaned_data

    def get_context_data(self, *args, **kwargs):
        default_language_code = 'en'
        # default_language = aims.language.objects.get(code=default_language_code)

        exists = True
        while exists:
            id_number = str(random.randint(0, 10000)).zfill(4)
            iati_identifier = 'MM-FERD-ID%s' % id_number
            exists = activity.objects.filter(iati_identifier=iati_identifier).exists()

        def prepare_language_fields(formset):
            if not formset[0].fields['language'].initial:
                formset[0].fields['language'].initial = default_language_code
            if not formset[1].fields['language'].initial:
                formset[1].fields['language'].initial = 'my'
                placeholder = {'placeholder': _('Myanmar language translation')}
                if 'title' in formset[1].fields:
                    formset[1].fields['title'].widget.attrs.update(placeholder)
                else:
                    formset[1].fields['description'].widget.attrs.update(placeholder)
            return formset

        context = super(CreateLocalActivity, self).get_context_data()

        context['editor'] = True
        context['form'] = kwargs['form']
        context['form'].fields['remote_data'].initial = ''
        context['form'].fields['iati_identifier'].initial = iati_identifier
        context['form'].fields['iati_identifier'].widget.attrs['readonly'] = True
        context['form'].fields['id'].initial = iati_identifier
        context['form_helper'] = forms.FormHelper()

        request_data = None
        if self.request.method == "POST":
            request_data = self.request.POST
        context['sections'] = aims_sections("CPU")

        title = forms.TitleFormset(request_data)
        description = forms.DescriptionFormset(request_data)
        objective = forms.ObjectivesFormset(request_data, prefix="objectives")
        target_groups = forms.TargetGroupsFormset(request_data, prefix="target_groups")

        context['title'] = prepare_language_fields(title)
        context['description'] = prepare_language_fields(description)
        context['objective'] = prepare_language_fields(objective)
        context['target_groups'] = prepare_language_fields(target_groups)

        context['activity_sector'] = forms.ActivitySectorFormset(request_data, queryset=aims.activity_sector.objects.exclude(sector__code__startswith=550), prefix="sector")
        context['activity_national_sector'] = forms.ActivityNationalSectorFormset(request_data, queryset=aims.activity_sector.objects.filter(sector__code__startswith=550), prefix="national_sector")

        context['ministry'] = forms.MinistryFormset(request_data, prefix="ministry", queryset=aims.activity_participating_organisation.objects.filter(role='Accountable'))
        context['participating_organisation'] = forms.ParticipatingOrganisationFormset(request_data, prefix="participating_organisation", queryset=aims.activity_participating_organisation.objects.exclude(role__in=("Accountable", "Funding")))
        context['location'] = forms.LocationFormset(request_data, prefix="location", )  # queryset=self.object.location_set.all())
        context['result'] = forms.ResultFormset(request_data, prefix="result")
        context['contact_info'] = forms.ContactFormset(request_data, prefix="contact_info")

        context['transactions'] = aims.transaction.aims.none()
        context['blank_transaction_form'] = forms.TransactionForm()

        return context

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data(form=form)

        inlinesets = [context['title'], context['description'], context['objective'], context['target_groups'],
                      context['ministry'], context['participating_organisation'],
                      context['activity_sector'],  # context['activity_national_sector'],
                      context['result'], context['location'], context['contact_info']]

        if form.is_valid():
            self.object = form.save()

            # Deal with many to many relationships which use 'through' intermediary class
            for policy_marker in context['form'].cleaned_data['policy_marker']:
                activity_policy_marker, created = aims.activity_policy_marker.objects.get_or_create(policy_marker=policy_marker, activity=self.object)
                activity_policy_marker.save()

            if 'participating_organisation' in context['form'].cleaned_data:
                role_accountable = organisation_role.objects.get(name="Accountable")
                for participating_organisation in context['form'].cleaned_data['participating_organisation']:
                    activity_participating_organisation, created = aims.activity_participating_organisation.objects.get_or_create(organisation=participating_organisation, activity=self.object, role=role_accountable)
                    activity_participating_organisation.save()

            # Deal with inline formsets
            for inlineset in inlinesets:
                if inlineset.is_valid():
                    inlineset.instance = self.object  # Can we delete this now?
                    for cleaned_data in inlineset.cleaned_data:
                        cleaned_data['activity_id'] = self.object.pk
                    try:
                        inlineset.save()
                    except:
                        pass
                else:
                    self.errors_found = True

            if hasattr(self, 'errors_found'):
                return self.render_to_response(self.get_context_data(form=form))

        return super(CreateLocalActivity, self).form_valid(form)


class EditActivity(SuccessMessageMixin, UpdateView):
    template_name = "aims/edit_data.html"
    form_class = forms.ActivityForm
    model = aims.activity
    success_message = _("Activity was saved successfully")

    def get_success_url(self):
        return "/activity/%s/" % self.object.iati_identifier

    def get_success_message(self, cleaned_data):
        if cleaned_data['is_draft']:
            self.success_message = _("Activity was successfully saved as a draft")
        return self.success_message % cleaned_data

    def check_is_draft(self, activity):
        try:
            user = self.request.user
            if activity.is_draft and not user.is_staff:
                if not user.userorganisation.organisations.filter(pk=activity.reporting_organisation.pk).exists():
                    raise Exception(_('Activity is defined as draft'))
        except:
            raise Http404(_('Activity not found'))

        return activity

    def get_object(self, queryset=None):

        # this should ensure backwards compatibility
        activity = aims.activity.aims.with_drafts().filter(iati_identifier=self.kwargs['iati_identifier'])

        if activity.exists():
            activity = activity.first()
        elif aims.activity.aims.filter(pk=self.kwargs['iati_identifier']).exists():
            activity = aims.activity.aims.filter(pk=self.kwargs['iati_identifier']).first()
        # else:
        #     return get_object_or_404(aims.activity.objects, iati_identifier=self.kwargs['iati_identifier'])

        return self.check_is_draft(activity)

    def get_initial(self):

        # this should ensure backwards compatibility
        self.object.iati_identifier = self.object.pk if not self.object.iati_identifier else self.object.iati_identifier

        initial = {'remote_data': self.object.pk}
        initial.update(self.object.__dict__)

        return initial

    def get_context_data(self, *args, **kwargs):

        default_language_code = 'en'
        default_language = aims.language.objects.get(code=default_language_code)

        def prepare_language_fields(formset):
            if not formset[0].fields['language'].initial:
                formset[0].fields['language'].initial = default_language_code
            if not formset[1].fields['language'].initial:
                formset[1].fields['language'].initial = 'my'
                placeholder = {'placeholder': _('Myanmar language translation')}
                if 'title' in formset[1].fields:
                    formset[1].fields['title'].widget.attrs.update(placeholder)
                else:
                    formset[1].fields['description'].widget.attrs.update(placeholder)
            return formset

        context = super(EditActivity, self).get_context_data()

        context['form'] = kwargs['form']
        context['form'].fields['remote_data'].initial = self.object.pk
        context['form_helper'] = forms.FormHelper()
        context['sections'] = aims_sections("CPU")

        # disable form fields for those who do not have permission
        editor = base_utils.check_editor_privilege(self.request.user, self.object.reporting_organisation)
        context['editor'] = editor

        context['form '] = disable_fields_in_form(context['form'], editor)

        request_data = None
        if self.request.method == "POST":
            request_data = self.request.POST

        for title in self.object.title_set.filter(language=None):
            title.language = default_language
            title.save()

        for description in self.object.description_set.filter(language=None):
            description.language = default_language
            description.save()

        title = forms.TitleFormset(request_data, instance=self.object, queryset=self.object.title_set.all().order_by('language'))
        title = disable_fields_in_formset(title, editor)
        description = forms.DescriptionFormset(request_data, instance=self.object, queryset=self.object.description_set.filter(type=1).order_by('language'))
        description = disable_fields_in_formset(description, editor)
        objective = forms.ObjectivesFormset(request_data, instance=self.object, prefix="objectives", queryset=self.object.description_set.filter(type=2).order_by('language'))
        objective = disable_fields_in_formset(objective, editor)
        target_groups = forms.TargetGroupsFormset(request_data, instance=self.object, prefix="target_groups", queryset=self.object.description_set.filter(type=3).order_by('language'))
        target_groups = disable_fields_in_formset(target_groups, editor)

        context['title'] = prepare_language_fields(title)
        context['description'] = prepare_language_fields(description)
        context['objective'] = prepare_language_fields(objective)
        context['target_groups'] = prepare_language_fields(target_groups)

        context['activity_sector'] = disable_fields_in_formset(forms.ActivitySectorFormset(request_data, instance=self.object, queryset=self.object.sectors, prefix="sector"), editor)
        context['activity_national_sector'] = disable_fields_in_formset(forms.ActivityNationalSectorFormset(request_data, instance=self.object, queryset=self.object.national_sectors, prefix="national_sector"), editor)

        context['ministry'] = disable_fields_in_formset(forms.MinistryFormset(request_data, instance=self.object, prefix="ministry", queryset=self.object.activity_participating_organisation_set.filter(role='Accountable')), editor)
        context['participating_organisation'] = disable_fields_in_formset(forms.ParticipatingOrganisationFormset(request_data, instance=self.object, prefix="participating_organisation", queryset=aims.activity_participating_organisation.objects.exclude(role="Accountable")), editor)
        context['location'] = disable_fields_in_formset(forms.LocationFormset(request_data, instance=self.object, prefix="location", ), editor)  # queryset=self.object.location_set.all())
        context['result'] = disable_fields_in_formset(forms.ResultFormset(request_data, instance=self.object, prefix="result", queryset=self.object.result_set), editor)
        context['contact_info'] = disable_fields_in_formset(forms.ContactFormset(request_data, instance=self.object, prefix="contact_info", queryset=self.object.contact_info_set.all()), editor)

        transactions = aims.transaction.aims.with_drafts().filter(activity=self.object.pk).order_by('-transaction_date')

        for transaction in transactions:
            auto_id = 'transaction_' + str(transaction.pk) + '_%s'
            transaction.modal_form = disable_fields_in_form(forms.TransactionForm(instance=transaction, auto_id=auto_id), editor)
        context['transactions'] = transactions
        context['blank_transaction_form'] = disable_fields_in_form(forms.TransactionForm(), editor)

        return context

    @transaction.atomic
    def form_valid(self, form):

        context = self.get_context_data(form=form)

        inlinesets = [context['title'], context['description'], context['objective'], context['target_groups'],
                      context['ministry'], context['participating_organisation'],
                      context['activity_sector'], context['activity_national_sector'],
                      context['result'], context['location'], context['contact_info']]

        if form.is_valid():
            self.object = form.save()

            # Deal with many to many relationships which use 'through' intermediary class
            # Delete policy markers saved already
            self.object.activity_policy_marker_set.all().delete()
            for policy_marker in context['form'].cleaned_data['policy_marker']:
                activity_policy_marker, created = aims.activity_policy_marker.objects.get_or_create(policy_marker=policy_marker, activity=self.object)
                activity_policy_marker.save()

            # role_accountable = organisation_role.objects.get(name="Accountable")
            # Delete participating organisation saved already
            # self.object.activity_participating_organisation_set.filter(organisation__code__icontains="MM-FERD-SWG").delete()
            # for participating_organisation in context['form'].cleaned_data['participating_organisation']:
            #     activity_participating_organisation, created = aims.activity_participating_organisation.objects.get_or_create(organisation=participating_organisation, activity=self.object, role=role_accountable)
            #     activity_participating_organisation.save()

            # Deal with inline formsets
            for inlineset in inlinesets:
                if inlineset.is_valid():
                    inlineset.instance = self.object
                    inlineset.save()
                else:
                    self.errors_found = True

            if hasattr(self, 'errors_found'):
                error_message = _("Activity was not saved")
                messages.error(self.request, error_message)
                return self.render_to_response(context)

        return super(EditActivity, self).form_valid(form)


class DeleteActivity(View):

    def post(self, *args, **kwargs):
        if self.request.is_ajax():
            if self.request.POST['object_type'] == 'activity':
                get_object_or_404(aims.activity.objects, pk=self.request.POST['pk']).delete()
            elif self.request.POST['object_type'] == 'transaction':
                get_object_or_404(aims.transaction.objects, pk=self.request.POST['pk']).delete()
            else:
                raise Http404

            success_message = _("Item was deleted successfully")
            messages.success(self.request, success_message)

            return HttpResponse(status=200)

        else:
            raise Http404


class EditOrganisation(SuccessMessageMixin, UpdateView):
    template_name = "aims/edit_data.html"
    form_class = forms.OrganisationForm
    model = aims.organisation
    success_message = _("Organisation was saved successfully")

    def get_success_url(self):
        return "/organisation/%s/" % self.object.pk

    def get_object(self, queryset=None):
        try:
            return get_object_or_404(aims.organisation.aims, pk=self.kwargs['pk'])
        except:
            return get_object_or_404(aims.organisation.objects, pk=self.kwargs['pk'])

    def get_initial(self):
        activity = aims.organisation.objects.get(pk=self.kwargs['pk'])
        initial = {'remote_data': self.kwargs['pk']}
        initial.update(activity.__dict__)
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super(EditOrganisation, self).get_context_data()

        editor = base_utils.check_editor_privilege(self.request.user, self.object)
        #editor = True if self.request.user.is_staff or self.request.user.userorganisation.organisations.filter(pk=self.object.pk) else False

        context['editor'] = editor
        context['form'] = kwargs['form']
        context['form'].fields['remote_data'].initial = self.kwargs['pk']
        context['form'] = disable_fields_in_form(context['form'], editor)

        context['form_helper'] = forms.FormHelper()

        return context


class CreateLocalTransaction(SuccessMessageMixin, CreateView):
    template_name = "aims/edit_data.html"
    form_class = forms.TransactionForm
    model = aims.transaction
    success_message = _("Transaction was saved successfully")

    def get_success_url(self):
        return "/activity/%s/" % self.object.activity.pk

    def get_context_data(self, *args, **kwargs):
        context = super(CreateLocalTransaction, self).get_context_data()

        editor = hasattr(self.object, 'activity') and base_utils.check_editor_privilege(self.request.user, self.object.activity.reporting_organisation)

        context['editor'] = editor
        context['form'] = kwargs['form']
        context['form_helper'] = forms.FormHelper()

        return context


class EditTransaction(SuccessMessageMixin, UpdateView):
    template_name = "aims/edit_data.html"
    form_class = forms.TransactionForm
    model = aims.transaction
    success_message = _("Transaction was saved successfully")

    def get_success_url(self):
        return "/activity/%s/" % self.object.activity.pk

    def get_object(self, queryset=None):
        try:
            transaction = aims.transaction.objects.with_drafts().get(pk=self.kwargs['pk'])
            return transaction
            #return get_object_or_404(aims.transaction.aims, pk=self.kwargs['pk'])
        except:
            return get_object_or_404(aims.transaction.objects, pk=self.kwargs['pk'])

    def get_initial(self):
        transaction = aims.transaction.objects.with_drafts().get(pk=self.kwargs['pk'])
        initial = {'remote_data': self.kwargs['pk']}
        initial.update(transaction.__dict__)
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super(EditTransaction, self).get_context_data()

        editor = base_utils.check_editor_privilege(self.request.user, self.object.activity.reporting_organisation)

        context['editor'] = editor
        context['form'] = kwargs['form']
        context['form'].fields['remote_data'].initial = self.kwargs['pk']
        context['form_helper'] = forms.FormHelper()

        return context

class HomeRedirectView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        reverse_location = reverse('aid_by', kwargs={'subset': 'CPU', 'section': 'location'})
        if not user.is_anonymous():
            if user.is_staff or not hasattr(user, 'userorganisation'):
                return reverse_location
            elif user.userorganisation.organisations.exists():
                return reverse('donor_profile', kwargs={'iati_identifier': user.userorganisation.organisations.first().pk})
            else:
                return reverse_location
        else:
            return reverse_location

class SearchView(AjaxListView, HayStackSearchView):

    template_name = 'search/search.html'
    page_template = 'search/result.html'
    form_class = forms.ActivitySearchForm
    load_all = True
    searchqueryset = None

    def get_queryset(self, *args, **kwargs):

        self.form = self.build_form()
        self.query = self.get_query()
        return self.get_results()

    def get_context_data(self, *args, **kwargs):

        context = super(SearchView, self).get_context_data(**kwargs)
        context['page_template'] = self.page_template
        context['form'] = self.form

        if self.request.is_ajax():
            self.template_name = self.page_template

        context['search_term'] = self.request.REQUEST['q'] or None

        return context
