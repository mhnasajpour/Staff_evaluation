from django.contrib import admin, messages
from .models import Survey, QuestionGroup, Question, QuestionAnswer
from Period.models import Period


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('period', 'type', 'is_done', 'respondent_position', 'target_position')
    search_fields = ('respondent_position', 'target_position')
    list_filter = ('period', 'type', 'is_done')
    fields = ('period', 'type', 'is_done', 'respondent_position', 'target_position')

@admin.register(QuestionGroup)
class QuestionGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('period', 'group', 'type', 'category', 'weight', 'content')
    search_fields = ('period', 'content')
    list_filter = ('period', 'group', 'type', 'category')
    fields = ('period', 'group', 'content', 'weight', 'type', 'category')
    actions = ('duplicate_questions',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(QuestionAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['category'].required = False
        return form
    
    
    @admin.action(description='Duplicate questions for current period')
    def duplicate_questions(modeladmin, request, queryset):
        for obj in queryset:
            Question.objects.create(group=obj.group, content=obj.content, period=Period.get_current_period(), weight=obj.weight, type=obj.type, category=obj.category)
        messages.success(request, "Successfully duplicated.")

@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('survey', 'question', 'answer')
    search_fields = ('survey', 'question__content')
    list_filter = ('survey__period', 'survey__type', 'answer')
    fields = ('survey', 'question', 'answer')
