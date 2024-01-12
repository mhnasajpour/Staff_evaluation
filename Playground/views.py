from django.shortcuts import render, redirect
from django.views import View
from .forms import ManagementForm
from User.staff_management import clean_and_create_data
from User.models import User
from Period.models import Period


class Home(View):
    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('user:login')
        user_categories = User.objects.get(
            pk=self.request.user.pk).categories.all()
        period_categories = Period.get_current_period().categories.all()
        categories = user_categories & period_categories
        if categories:
            return redirect('playground:question_answers', category=categories.first().name)
        else:
            return render(request, 'Playground/question-answers.html')


class Question_answers(View):
    def get(self, request, category):
        if not self.request.user.is_authenticated:
            return redirect('auth/login')

        user_categories = User.objects.get(
            pk=self.request.user.pk).categories.all()
        period_categories = Period.get_current_period().categories.all()
        categories = (user_categories & period_categories)

        category = category if category in categories.values_list(
            'name', flat=True) else None

        context = {
            'categories': categories.values_list('name', flat=True),
            'current_category': category,
        }
        return render(request, 'Playground/question-answers.html', context=context)


class Management(View):
    def get(self, request):
        form = ManagementForm()
        return render(request, 'Playground/admin.html', {'form': form})

    def post(self, request):
        clean_and_create_data(request.FILES['user_file'])
        # return render(request, 'User/login.html', {'form': form, 'error': True})
