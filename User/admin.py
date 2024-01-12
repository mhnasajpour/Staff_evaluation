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
    list_display = ('personnel_code', 'first_name',
                    'last_name', 'national_code')
    search_fields = ('personnel_code', 'first_name',
                     'last_name', 'national_code')
    fields = ('username', 'password', 'personnel_code',
              'national_code', 'first_name', 'last_name', 'is_active')
    inlines = (userInlineAdmin, ManagerInlineAdmin)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit', 'user', 'manager', 'category')
    search_fields = ('title', 'unit', 'user', 'manager')
    list_filter = ('category', 'unit')
    fields = ('title', 'unit', 'user', 'manager', 'category')
