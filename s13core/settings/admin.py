from django.contrib import admin, messages
from .models import Setting, ContactInfo, CopyrightInfo, Disclaimer, \
    ValidationError


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Settings', {
            'fields': (('name', 'is_active'), 'title', 'description',
                       ('keywords', 'append_keywords')),
        }),
        ('No Homepage Settings', {
            'fields': (('nohome_content_type', 'nohome_content_items'),
                       'nohome_title', 'nohome_custom'),
        }),
        ('Head Elements', {
            'fields': ('css', 'js'),
        }),
        ('Footer Information', {
            'fields': ('copyright', 'contact', 'disclaimer'),
        }),
    )

    def get_actions(self, request):
        '''Disables delete_selected because it overrides our delete method.'''

        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_model(self, request, obj):
        try:
            obj.delete()
        except ValidationError as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e.message)
        except:
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'An unknown error occurred.')


@admin.register(ContactInfo)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(CopyrightInfo)
class CopyrightInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(Disclaimer)
class DisclaimerAdmin(admin.ModelAdmin):
    pass
