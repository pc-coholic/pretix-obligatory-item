from django.conf.urls import url

from pretix_obligatory_item.views import ObligatoryItemSettings

urlpatterns = [
    url(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/obligatory_item/$',
        ObligatoryItemSettings.as_view(), name='settings'),
]
