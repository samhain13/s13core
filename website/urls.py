from django.urls import include, path


urlpatterns = [
    path(
        's13admin/',
        include(
            ('s13core.administration.urls', 's13core.administration'),
            namespace='s13admin'
        )
    ),
    # Default route.
    path(
        '',
        include(
            ('s13core.content_management.urls', 's13core.content_management'),
            namespace='s13cms'
        )
    ),
]
