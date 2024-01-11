from django.contrib import admin
from .models import Group, User


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_root')
    search_fields = ('name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'national_code', 'first_name',
                    'last_name', 'parent_id')
    search_fields = ('national_code', 'first_name', 'last_name', 'parent_id')
    list_filter = ('positions',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['parent_id'].required = False
        form.base_fields['positions'].required = False
        return form
