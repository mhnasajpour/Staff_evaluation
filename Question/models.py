from django.db import models
from Period.models import Period
from User.models import Group
from django.core.exceptions import ValidationError


TYPE_CHOICES = (
    ('0', 'خود ارزیابی'),
    ('1', 'ارزشیابی مدیر'),
    ('2', 'ارزشیابی همکار'),
    ('3', 'ارزشیابی هم‌رسته'),
    ('4', 'ارزشیابی تخصصی')
)


class Question(models.Model):
    context = models.CharField(max_length=300)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    weight = models.FloatField(default=1)
    type = models.CharField(choices=TYPE_CHOICES, max_length=1, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def clean(self):
        if self.type != '4' and self.group:
            raise ValidationError(
                f'تایپ سوال "{TYPE_CHOICES[int(self.type)][1]}"، نیازی به گروه شغلی ندارد')
        if self.type == '4' and self.group not in self.period.groups.all():
            raise ValidationError(
                f'دوره زمانی "{self.period}"، شامل گروه "{self.group}" نمی‌باشد')
        return super().clean()
