from django.shortcuts import render
from django.views import View
from Playground.forms import ManagementForm
from Period.models import Period
from .survey_management import clean_and_create_surveys


class Renew_surveys(View):
    def get(self, request):
        if not self.request.user.is_superuser:
            return None
        form = ManagementForm()
        current_period = Period.get_current_period()
        if not current_period:
            return render(request, 'Playground/admin.html', {'form': form, 'status': False, 'message': 'هیچ دوره زمانی ارزشیابی فعالی وجود ندارد. لطفا ابتدا دوره ارزشیابی تعریف کنید'})
        try:
            clean_and_create_surveys(current_period)
        except:
            return render(request, 'Playground/admin.html', {'form': form, 'status': False, 'message': 'بدلیل وجود خطا، پرسشنامه‌ها ایجاد نشدند. لطفا مجددا تلاش کنید.'})
        return render(request, 'Playground/admin.html', {'form': form, 'status': True, 'message': 'پرسشنامه‌ها با موفقیت ایجاد شدند.'})
