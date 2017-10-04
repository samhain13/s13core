from django.conf import settings
from django.conf.urls import url
from s13core.content_management import views as v

urlpatterns = [
    url(r'^keyword-search/$',
        v.KeywordSearchView.as_view(),
        name='keyword-search'),
    url(r'^(?P<section_slug>[\w\-]+)/(?P<article_slug>[\w\-]+)/$',
        v.ArticleView.as_view(),
        name='article'),
    url(r'^(?P<section_slug>[\w\-]+)/$',
        v.SectionView.as_view(),
        name='section'),
    url(r'^$',
        v.HomepageView.as_view(),
        name='homepage'),
]

if settings.DEBUG:
    urlpatterns.insert(
        0,
        url(
            r'^ui-tester/(?P<page>[\w\-\.]+)$',
            v.UITestView.as_view(),
            name='ui_tester'
        )
    )
    urlpatterns.insert(
        0,
        url(
            r'^ui-tester/$',
            v.UITestView.as_view(),
            name='ui_tester'
        )
    )
