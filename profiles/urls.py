from django.conf.urls import patterns, url

from profiles import views

urlpatterns = patterns('',
    url(r'^donor/$', views.OrganisationProfile.as_view(), name='donor_profile'),
    url(r'^update/', views.UpdateGeneric.as_view(), name='update'),
    url(r'^upload/', views.UploadGeneric.as_view(), name='upload'),
    url(r'^activity/$', views.ActivityProfile.as_view(), name='activity_profile'),
    url(r'^donor/(?P<iati_identifier>[^/]+)/', views.OrganisationProfile.as_view(), name='donor_profile'),
    url(r'^activity/(?P<iati_identifier>[^/]+)/$', views.ActivityProfile.as_view(), name='activity_profile'),
    url(r'^save-contact/(?P<pk>[\d]+)/$', views.SaveContact.as_view(), name='save_contact'),
    url(r'^create-person/$', views.CreatePerson.as_view(), name='create_person'),
    url(r'^update-person/(?P<pk>[\d]+)/$', views.UpdatePerson.as_view(), name='update_person'),
    url(r'^fetch-person/(?P<pk>[\d]+)/?$', views.PersonView.as_view(), name='fetch_person'),
    url(r'^fetch-contact/(?P<pk>[\d]+)/?$', views.ContactView.as_view(), name='fetch_contact'),
    url(r'^fetch-data/(?P<pk>[\d]+)/?$', views.PersonData.as_view(), name='person_data'),
    url(r'^delete-person/(?P<pk>[\d]+)/?$', views.DeletePerson.as_view(), name='delete_person'),
    url(r'^reorder-people/$', views.ReorderPeople.as_view(), name='reorder_people'),
)