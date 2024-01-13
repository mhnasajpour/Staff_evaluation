from django.shortcuts import render, redirect
from django.views import View
from Playground.forms import ManagementForm
from Period.models import Period
from User.models import Position
from .models import Survey

def create_self_and_manager_assessment_surveys(period):
    allowed_categories = period.categories.values_list('name', flat=True)
    positions = Position.objects.filter(category__is_root=False, category__name__in=allowed_categories)
    for position in positions:
        Survey.objects.create(period=period, target_position=position, respondent_position=position, type='0')
        Survey.objects.create(period=period, target_position=position, respondent_position=position, type='1')

def create_colleague_assessment_surveys(period):
    allowed_categories = period.categories.values_list('name', flat=True)
    positions = Position.objects.filter(category__is_root=False, category__name__in=allowed_categories)

class Renew_surveys(View):
    def get(self, request):
        if self.request.user.is_superuser:
            form = ManagementForm()
            current_period = Period.get_current_period()
            if not current_period:
                return render(request, 'Playground/admin.html', {'form': form, 'status': False, 'message': 'هیچ دوره زمانی ارزشیابی فعالی وجود ندارد. لطفا ابتدا دوره ارزشیابی تعریف کنید'})
            try:
                Survey.objects.all().filter(period=current_period).delete()
                create_self_and_manager_assessment_surveys(current_period)
                create_colleague_assessment_surveys(current_period)
            except:
                return render(request, 'Playground/admin.html', {'form': form, 'status': False, 'message': 'بدلیل وجود خطا، پرسشنامه‌ها ایجاد نشدند. لطفا مجددا تلاش کنید.'})
            return render(request, 'Playground/admin.html', {'form': form, 'status': True, 'message': 'پرسشنامه‌ها با موفقیت ایجاد شدند.'})
