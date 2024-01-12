from django.db import models
from datetime import date
from User.models import Category
from django.core.exceptions import ValidationError


class Period(models.Model):
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError(
                "تاریخ شروع دوره زمانی، نمی‌تواند از دوره پایانی آن بزرگتر باشد.")
        for start, end in Period.objects.values_list("start_date", "end_date"):
            if start <= self.start_date <= end or start <= self.end_date <= end or self.start_date <= start <= self.end_date:
                raise ValidationError(
                    "دو دوره زمانی نمی‌توانند از لحاظ زمانی همپوشانی داشته باشند.")
        return super().clean()

    def get_current_period():
        return Period.objects.get(start_date__lte=date.today(), end_date__gte=date.today())
