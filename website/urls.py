from django.conf.urls import include, url


urlpatterns = [
    url(
        r'^s13admin/',
        include('s13core.administration.urls', namespace='s13admin')
    ),
    url(
        r'^s13msgs/',
        include('s13core.messaging.urls', namespace='s13messaging')
    ),
    # Default route.
    url(
        r'^',
        include('s13core.content_management.urls', namespace='s13cms')
    ),
]
