from django.conf.urls import url

from . import views as v

urlpatterns = [
    url(r'^sitemessages/$',
        v.SiteMessageCreate.as_view(),
        name='sitemessage-form'),
]
