from django.shortcuts import render, redirect
from django.views import View
from User.models import User
from Period.models import Period


class home(View):
    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('auth/login')
        user_groups = User.objects.get(pk=self.request.user.pk).positions.all()
        supported_groups = Period.get_current_period().groups.all()
        context = {'groups': (
            user_groups & supported_groups).values_list('id', 'name')}
        return render(request, 'Playground/home.html', context=context)
