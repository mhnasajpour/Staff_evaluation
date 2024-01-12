from django.shortcuts import render, redirect
from django.views import View
from .forms import ManagementForm
from User.staff_management import clean_and_create_data
from User.models import User, Position
from Period.models import Period


def get_user_categories(user_id):
    user_categories = Position.objects.filter(user_id=user_id).values_list('category__name', flat=True)
    period_categories = Period.get_current_period().categories.values_list('name', flat=True)
    return set(user_categories).intersection(period_categories)

class Home(View):
    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('user:login')
        category = get_user_categories(self.request.user.id)
        if category:
            return redirect('playground:question_answers', category=category.pop())
        else:
            return render(request, 'Playground/question-answers.html')


class Question_answers(View):
    def get(self, request, category, questionType):
        if not self.request.user.is_authenticated:
            return redirect('auth/login')
        categories = get_user_categories(self.request.user.id)
        category = category if category in categories else None
        user_position = Position.objects.get(user_id=self.request.user.id, category__name=category) if category else None
        context = {
            'categories': categories,
            'current_category': category,
            'position': user_position,
            'questionType': questionType,
        }
        return render(request, 'Playground/question-answers.html', context=context)


class Management(View):
    def get(self, request):
        form = ManagementForm()
        return render(request, 'Playground/admin.html', {'form': form})

    def post(self, request):
        form = ManagementForm()
        try:
            clean_and_create_data(request.FILES['user_file'])
        except:
            return render(request, 'Playground/admin.html', {'form': form, 'status': False})
        return render(request, 'Playground/admin.html', {'form': form, 'status': True})
        
            
