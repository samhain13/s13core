from django.urls import path

from .views import articles
from .views import fileassets
from .views import home
from .views import settings


urlpatterns = [
    # ------------- Contents views.
    path(
        'articles/',
        articles.ArticlesList.as_view(),
        name='articles'
    ),
    path(
        'articles/detail/<int:pk>/',
        articles.ArticleDetail.as_view(),
        name='detail_article'
    ),
    path(
        'articles/detail/<int:pk>/<str:mode>/',
        articles.ArticleDetail.as_view(),
        name='detail_article'
    ),
    path(
        'articles/<str:action>/<str:mode>/<int:pk>/<int:xpk>/',
        articles.ArticleAssociate.as_view(),
        name='associate_article'
    ),

    path(
        'articles/create-article/',
        articles.ArticleCreate.as_view(),
        name='create_article'
    ),
    path(
        'articles/create-article/<int:parent_pk>',
        articles.ArticleCreate.as_view(),
        name='create_article'
    ),
    path(
        'articles/delete-article/<int:pk>/',
        articles.ArticleDelete.as_view(),
        name='delete_article'
    ),
    path(
        'articles/update-article/<int:pk>/',
        articles.ArticleUpdate.as_view(),
        name='update_article'
    ),

    path(
        'fileassets/',
        fileassets.FileAssetsList.as_view(),
        name='fileassets'
    ),
    path(
        'fileassets/create-fileasset/',
        fileassets.FileAssetCreate.as_view(),
        name='create_fileasset'
    ),
    path(
        'fileassets/delete-fileasset/<int:pk>/',
        fileassets.FileAssetDelete.as_view(),
        name='delete_fileasset'
    ),
    path(
        'fileassets/update-fileasset/<int:pk>/',
        fileassets.FileAssetUpdate.as_view(),
        name='update_fileasset'
    ),

    # ------------- Settings views.
    path(
        'settings/',
        settings.SettingsList.as_view(),
        name='settings'
    ),
    path(
        'settings/create-settings/',
        settings.SettingsCreate.as_view(),
        name='create_settings'
    ),
    path(
        'settings/delete-settings/<int:pk>/',
        settings.SettingsDelete.as_view(),
        name='delete_settings'
    ),
    path(
        'settings/update-settings/<int:pk>/',
        settings.SettingsUpdate.as_view(),
        name='update_settings'
    ),

    path(
        'settings/contact-info/',
        settings.ContactInfoList.as_view(),
        name='contact_info'
    ),
    path(
        'settings/create-contact-info/',
        settings.ContactInfoCreate.as_view(),
        name='create_contact_info'
    ),
    path(
        'settings/delete-contact-info/<int:pk>/',
        settings.ContactInfoDelete.as_view(),
        name='delete_contact_info'
    ),
    path(
        'settings/update-contact-info/<int:pk>/',
        settings.ContactInfoUpdate.as_view(),
        name='update_contact_info'
    ),

    path(
        'settings/copyright-info/',
        settings.CopyrightInfoList.as_view(),
        name='copyright_info'
    ),
    path(
        'settings/create-copyright-info/',
        settings.CopyrightInfoCreate.as_view(),
        name='create_copyright_info'
    ),
    path(
        'settings/delete-copyright-info/<int:pk>/',
        settings.CopyrightInfoDelete.as_view(),
        name='delete_copyright_info'
    ),
    path(
        'settings/update-copyright-info/<int:pk>/',
        settings.CopyrightInfoUpdate.as_view(),
        name='update_copyright_info'
    ),

    path(
        'settings/disclaimer/',
        settings.DisclaimerList.as_view(),
        name='disclaimer'
    ),
    path(
        'settings/create-disclaimer/',
        settings.DisclaimerCreate.as_view(),
        name='create_disclaimer'
    ),
    path(
        'settings/delete-disclaimer/<int:pk>/',
        settings.DisclaimerDelete.as_view(),
        name='delete_disclaimer'
    ),
    path(
        'settings/update-disclaimer/<int:pk>/',
        settings.DisclaimerUpdate.as_view(),
        name='update_disclaimer'
    ),

    # ------------- Admin home views.
    path(
        'login/',
        home.Login.as_view(),
        name='login'
    ),
    path(
        'logout/',
        home.Logout.as_view(),
        name='logout'
    ),
    path(
        'update-password/<int:pk>/',
        home.UpdatePassword.as_view(),
        name='update_password'
    ),
    path(
        'update-user-info/<int:pk>/',
        home.UpdateUserInformation.as_view(),
        name='update_user_info'
    ),

    # Default route.
    path(
        '',
        home.Dashboard.as_view(),
        name='dashboard'
    ),
]
