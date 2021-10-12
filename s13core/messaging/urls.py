from django.urls import path

from . import views as v

urlpatterns = [
    path(
        'sitemessages/',
        v.SiteMessageCreate.as_view(),
        name='sitemessage-form'
    ),
]
