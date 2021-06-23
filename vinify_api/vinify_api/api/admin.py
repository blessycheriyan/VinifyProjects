from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from authemail.admin import EmailUserAdmin

from .models import VerifiedUser


class MyUserAdmin(EmailUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'is_verified', 'groups',
                                       'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Custom info'), {'fields': ('date_of_birth',)}),
    )


class VerifiedUserAdmin(MyUserAdmin):
    def has_add_permission(self, request):
        return False


admin.site.unregister(get_user_model())
admin.site.register(get_user_model())
admin.site.register(VerifiedUser, VerifiedUserAdmin)

from django.contrib import admin

from django.apps import apps
from django.contrib import admin
from api.models import   wine,Wines

admin.site.register(Wines)
app = apps.get_app_config('api')

for model_name, model in app.models.items():
    print(model_name)
    if model_name != "wine":

        try:
            admin.site.register(model)
        except:
            pass


