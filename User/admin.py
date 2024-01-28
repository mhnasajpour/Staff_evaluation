from django.contrib import admin
from .models import Category, User, Position


class userInlineAdmin(admin.TabularInline):
    model = Position
    fk_name = 'user'
    extra = 0

class ManagerInlineAdmin(admin.TabularInline):
    model = Position
    fk_name = 'manager'
    extra = 0

class PositionInlineAdmin(admin.TabularInline):
    model = Position
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_root')
    search_fields = ('name',)
    fields = ('name', 'is_root')
    inlines = (PositionInlineAdmin,)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('personnel_code', 'first_name', 'last_name', 'national_code')
    search_fields = ('personnel_code', 'first_name', 'last_name', 'national_code')
    fields = ('username', 'password', 'personnel_code', 'national_code', 'first_name', 'last_name', 'is_active')
    inlines = (userInlineAdmin, ManagerInlineAdmin)

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit', 'user', 'manager', 'category', 'is_active')
    search_fields = ('title', 'unit', 'user', 'manager')
    list_filter = ('category', 'unit', 'is_active')
    fields = ('title', 'unit', 'user', 'manager', 'category', 'is_active')

    def get_form(self, request, obj=None, **kwargs):
        form = super(PositionAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['title'].required = False
        form.base_fields['unit'].required = False
        form.base_fields['manager'].required = False
        form.base_fields['category'].required = False
        return form