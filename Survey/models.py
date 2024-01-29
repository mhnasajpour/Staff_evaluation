from django.db import models
from Period.models import Period
from User.models import Category, Position
from django.core.exceptions import ValidationError


TYPE_CHOICES = (
    ('0', 'خود ارزیابی'),
    ('1', 'ارزشیابی مدیر'),
    ('2', 'ارزشیابی کارمند'),
    ('3', 'ارزشیابی همکار'),
    ('4', 'ارزشیابی هم‌رسته'),
    ('5', 'ارزشیابی تخصصی'),
)

ANSWER_CHOICES = (
    (1, 'ضعیف'),
    (2, 'متوسط'),
    (3, 'خوب'),
    (4, 'بسیار خوب')
)

class Survey(models.Model):
    period = models.ForeignKey(Period, on_delete=models.SET_NULL, null=True)
    respondent_position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name='respondent_set')
    target_position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name='target_set')
    type = models.CharField(choices=TYPE_CHOICES, max_length=1, null=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.target_position.user.get_full_name() + ' <- ' + self.respondent_position.user.get_full_name()


class QuestionGroup(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Question(models.Model):
    group = models.ForeignKey(QuestionGroup, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=300)
    period = models.ForeignKey(Period, on_delete=models.SET_NULL, null=True)
    weight = models.FloatField(default=1)
    type = models.CharField(choices=TYPE_CHOICES, max_length=1, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        MAX_LENGTH = 50
        return '... ' + self.content[:MAX_LENGTH] if len(self.content) > MAX_LENGTH else self.content

    def clean(self):
        if self.type != '5' and self.category:
            raise ValidationError(
                f'تایپ سوال "{TYPE_CHOICES[int(self.type)][1]}"، نیازی به گروه شغلی ندارد')
        if self.type == '5' and self.category not in self.period.categories.all():
            raise ValidationError(
                f'دوره زمانی "{self.period}"، شامل گروه "{self.category}" نمی‌باشد')
        return super().clean()

class QuestionAnswer(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    answer = models.IntegerField(choices=ANSWER_CHOICES, null=True)