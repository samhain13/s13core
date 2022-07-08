from django.conf import settings
from django.urls import path
from s13core.content_management import views as v

urlpatterns = [
    path(
        'keyword-search/',
        v.KeywordSearchView.as_view(),
        name='keyword-search'
    ),
    path(
        'sitemap/',
        v.SitemapView.as_view(),
        name='sitemap'
    ),
    path(
        '<str:section_slug>/<str:article_slug>/',
        v.ArticleView.as_view(),
        name='article'
    ),
    path(
        '<str:section_slug>/',
        v.SectionView.as_view(),
        name='section'
    ),
    path(
        '',
        v.HomepageView.as_view(),
        name='homepage'
    ),
]

if settings.DEBUG:
    urlpatterns.insert(
        0,
        path(
            'ui-tester/<str:page>',
            v.UITestView.as_view(),
            name='ui_tester'
        )
    )
    urlpatterns.insert(
        0,
        path(
            'ui-tester/',
            v.UITestView.as_view(),
            name='ui_tester'
        )
    )
