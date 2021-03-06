from django.conf.urls import url

from .views import articles
from .views import fileassets
from .views import home
from .views import settings
from .views import socmed


urlpatterns = [
    # ------------- Contents views.
    url(
        r'^articles/$',
        articles.ArticlesList.as_view(),
        name='articles'
    ),
    url(
        r'^articles/detail/(?P<pk>[\d]+)/$',
        articles.ArticleDetail.as_view(),
        name='detail_article'
    ),
    url(
        r'^articles/detail/(?P<pk>[\d]+)/(?P<mode>[\w\-]+)/$',
        articles.ArticleDetail.as_view(),
        name='detail_article'
    ),
    url(
        r'^articles/(?P<action>(add|remove))/(?P<mode>[\w\-]+)/' +
        '(?P<pk>[\d]+)/(?P<xpk>[\d]+)/$',
        articles.ArticleAssociate.as_view(),
        name='associate_article'
    ),

    url(
        r'^articles/create-article/$',
        articles.ArticleCreate.as_view(),
        name='create_article'
    ),
    url(
        r'^articles/create-article/(?P<parent_pk>[\d]+)$',
        articles.ArticleCreate.as_view(),
        name='create_article'
    ),
    url(
        r'^articles/delete-article/(?P<pk>[\d]+)/$',
        articles.ArticleDelete.as_view(),
        name='delete_article'
    ),
    url(
        r'^articles/update-article/(?P<pk>[\d]+)/$',
        articles.ArticleUpdate.as_view(),
        name='update_article'
    ),

    url(
        r'^fileassets/$',
        fileassets.FileAssetsList.as_view(),
        name='fileassets'
    ),
    url(
        r'^fileassets/create-fileasset/$',
        fileassets.FileAssetCreate.as_view(),
        name='create_fileasset'
    ),
    url(
        r'^fileassets/delete-fileasset/(?P<pk>[\d]+)/$',
        fileassets.FileAssetDelete.as_view(),
        name='delete_fileasset'
    ),
    url(
        r'^fileassets/update-fileasset/(?P<pk>[\d]+)/$',
        fileassets.FileAssetUpdate.as_view(),
        name='update_fileasset'
    ),

    # ------------- Social Media Collector views.
    url(
        r'^social-media/api-keys/$',
        socmed.APIKeyList.as_view(),
        name='socmedapikeys'
    ),
    url(
        r'^social-media/create-api-key/$',
        socmed.APIKeyCreate.as_view(),
        name='socmedapikeys_create'
    ),
    url(
        r'^social-media/delete-api-key/(?P<pk>[\d]+)/$',
        socmed.APIKeyDelete.as_view(),
        name='socmedapikeys_delete'
    ),
    url(
        r'^social-media/update-api-key/(?P<pk>[\d]+)/$',
        socmed.APIKeyUpdate.as_view(),
        name='socmedapikeys_update'
    ),
    url(
        r'^social-media/feeds/$',
        socmed.SocMedFeedList.as_view(),
        name='socmedfeeds'
    ),
    url(
        r'^social-media/create-feed/$',
        socmed.SocMedFeedCreate.as_view(),
        name='socmedfeeds_create'
    ),
    url(
        r'^social-media/delete-feed/(?P<pk>[\d]+)/$',
        socmed.SocMedFeedDelete.as_view(),
        name='socmedfeeds_delete'
    ),
    url(
        r'^social-media/update-feed/(?P<pk>[\d]+)/$',
        socmed.SocMedFeedUpdate.as_view(),
        name='socmedfeeds_update'
    ),
    url(
        r'^social-media/processors/$',
        socmed.SocMedProcessorList.as_view(),
        name='socmedprocessors'
    ),
    url(
        r'^social-media/create-processor/$',
        socmed.SocMedProcessorCreate.as_view(),
        name='socmedprocessors_create'
    ),
    url(
        r'^social-media/delete-processor/(?P<pk>[\d]+)/$',
        socmed.SocMedProcessorDelete.as_view(),
        name='socmedprocessors_delete'
    ),
    url(
        r'^social-media/update-processor/(?P<pk>[\d]+)/$',
        socmed.SocMedProcessorUpdate.as_view(),
        name='socmedprocessors_update'
    ),
    url(
        r'^social-media/retrieve-feed/(?P<pk>[\d]+)/$',
        socmed.RetrieveSocMedFeed.as_view(),
        name='socmed_retrieve'
    ),

    # ------------- Settings views.
    url(
        r'^settings/$',
        settings.SettingsList.as_view(),
        name='settings'
    ),
    url(
        r'^settings/create-settings/$',
        settings.SettingsCreate.as_view(),
        name='create_settings'
    ),
    url(
        r'^settings/delete-settings/(?P<pk>[\d]+)/$',
        settings.SettingsDelete.as_view(),
        name='delete_settings'
    ),
    url(
        r'^settings/update-settings/(?P<pk>[\d]+)/$',
        settings.SettingsUpdate.as_view(),
        name='update_settings'
    ),

    url(
        r'^settings/contact-info/$',
        settings.ContactInfoList.as_view(),
        name='contact_info'
    ),
    url(
        r'^settings/create-contact-info/$',
        settings.ContactInfoCreate.as_view(),
        name='create_contact_info'
    ),
    url(
        r'^settings/delete-contact-info/(?P<pk>[\d]+)/$',
        settings.ContactInfoDelete.as_view(),
        name='delete_contact_info'
    ),
    url(
        r'^settings/update-contact-info/(?P<pk>[\d]+)/$',
        settings.ContactInfoUpdate.as_view(),
        name='update_contact_info'
    ),

    url(
        r'^settings/copyright-info/$',
        settings.CopyrightInfoList.as_view(),
        name='copyright_info'
    ),
    url(
        r'^settings/create-copyright-info/$',
        settings.CopyrightInfoCreate.as_view(),
        name='create_copyright_info'
    ),
    url(
        r'^settings/delete-copyright-info/(?P<pk>[\d]+)/$',
        settings.CopyrightInfoDelete.as_view(),
        name='delete_copyright_info'
    ),
    url(
        r'^settings/update-copyright-info/(?P<pk>[\d]+)/$',
        settings.CopyrightInfoUpdate.as_view(),
        name='update_copyright_info'
    ),

    url(
        r'^settings/disclaimer/$',
        settings.DisclaimerList.as_view(),
        name='disclaimer'
    ),
    url(
        r'^settings/create-disclaimer/$',
        settings.DisclaimerCreate.as_view(),
        name='create_disclaimer'
    ),
    url(
        r'^settings/delete-disclaimer/(?P<pk>[\d]+)/$',
        settings.DisclaimerDelete.as_view(),
        name='delete_disclaimer'
    ),
    url(
        r'^settings/update-disclaimer/(?P<pk>[\d]+)/$',
        settings.DisclaimerUpdate.as_view(),
        name='update_disclaimer'
    ),

    # ------------- Admin home views.
    url(
        r'^login/$',
        home.Login.as_view(),
        name='login'
    ),
    url(
        r'^logout/$',
        home.Logout.as_view(),
        name='logout'
    ),
    url(
        r'^update-password/(?P<pk>[\d]+)/$',
        home.UpdatePassword.as_view(),
        name='update_password'
    ),
    url(
        r'^update-user-info/(?P<pk>[\d]+)/$',
        home.UpdateUserInformation.as_view(),
        name='update_user_info'
    ),

    # Default route.
    url(
        r'^$',
        home.Dashboard.as_view(),
        name='dashboard'
    ),
]
