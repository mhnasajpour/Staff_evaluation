from django.contrib import admin
from .models import Survey, Question, QuestionAnswer


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('period', 'type', 'is_done', 'respondent_position', 'target_position')
    search_fields = ('respondent_position', 'target_position')
    list_filter = ('period', 'type', 'is_done')
    fields = ('period', 'type', 'is_done', 'respondent_position', 'target_position')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('period', 'content', 'weight', 'type', 'category')
    search_fields = ('period', 'content')
    list_filter = ('period', 'type', 'category')
    fields = ('period', 'content', 'weight', 'type', 'category')

    def get_form(self, request, obj=None, **kwargs):
        form = super(QuestionAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['category'].required = False
        return form

@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('survey', 'question', 'answer')
    search_fields = ('survey', 'question__content')
    list_filter = ('survey__period', 'survey__type', 'answer')
    fields = ('survey', 'question', 'answer')
