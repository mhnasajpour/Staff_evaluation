from django.contrib import admin
from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('period', 'context', 'weight', 'type', 'category')
    search_fields = ('period', 'context')
    list_filter = ('period', 'type', 'category')

    def get_form(self, request, obj=None, **kwargs):
        form = super(QuestionAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['category'].required = False
        return form
