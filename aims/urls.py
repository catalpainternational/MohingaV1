from django.conf.urls import patterns, url, include
from django.conf import settings

from django.contrib.auth.decorators import login_required

from haystack.views import SearchView
from aims import views, forms


aid_by_urls = patterns('',
                       url(r"^(?P<subset>[ICPU]+)/(?P<section>location|sector|ministry|donor)/$",
                           login_required(views.AidBy.as_view()), name='aid_by'),
                       url(r"^(?P<subset>[ICPU]+)/(?P<section>location|sector|ministry|donor)/(?P<which>[\w-]+)$",
                           login_required(views.AidBy.as_view()), name='aid_by'),
                       url(r"^(?P<subset>[ICPU]+)/(?P<section>location|sector|ministry|donor)/(?P<which>[\w-]+)/(?P<specific>[\w-]+)$",
                           login_required(views.AidBy.as_view()), name='aid_by'),
                       )

urlpatterns = patterns('',
                       url(r"^$", views.HomeRedirectView.as_view(), name='index'),
                       url(r"^home/$", views.HomeRedirectView.as_view(), name='home'),
                       url(r"^dashboard/", include(aid_by_urls)),
                       url(r"^export/(?P<export>CSV|PDF)/",
                           include(aid_by_urls, namespace="export")),

                       url(r"^exports/(?P<method>[\w]+)/(?P<subset>[CPUI]+)/$",
                           login_required(views.Exporter.as_view()), name='export'),
                       url(r"^exports/(?P<method>[\w]+)/(?P<subset>[CPUI]+)/(?P<filter_name>[\w]+)/(?P<filter_value>[\w\d-]+)/$",
                           login_required(views.Exporter.as_view()), name='export'),
                       url(r"^exports/(?P<method>[\w]+)/(?P<subset>[CPUI]+)/(?P<section>[\w]+)/$",
                           login_required(views.Exporter.as_view()), name='export'),
                       url(r"^exports/(?P<method>[\w]+)/(?P<subset>[CPUI]+)/(?P<section>[\w]+)/(?P<filter_name>[\w]+)/(?P<filter_value>[\w\d-]+)/$",
                           login_required(views.Exporter.as_view()), name='export'),

                       url(r'^activity/new/$', login_required(views.CreateLocalActivity.as_view()),
                           name='create_activity'),
                       url(r'^activity/(?P<iati_identifier>[\w-]+)/$',
                           login_required(views.EditActivity.as_view()), name='edit_activity'),
                       url(r'^activity/(?P<iati_identifier>[\w-]+)/delete/$',
                           login_required(views.DeleteActivity.as_view()), name='delete_activity'),
                       url(r'^organisation/(?P<pk>[\w-]+)/',
                           login_required(views.EditOrganisation.as_view()), name='edit_organisation'),
                       url(r'^transaction/new/$', login_required(views.CreateLocalTransaction.as_view()),
                           name='create_transaction'),
                       url(r'^transaction/(?P<pk>[\w-]+)/',
                           login_required(views.EditTransaction.as_view()), name='edit_transaction'),

                       url(r'^accounts/', include('registration.urls')),
                       )

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
                            url(r'^rosetta/', include('rosetta.urls')),
                            )

if 'haystack' in settings.INSTALLED_APPS:
    # urlpatterns += patterns('',
    #                         url(r'^search/', SearchView(form_class=forms.ActivitySearchForm),
    #                             name='search'),
    #                         )

    urlpatterns += patterns('',
                            url(r'^search/', views.SearchView.as_view(), name='search'),
                            )

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += patterns('',
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     )
