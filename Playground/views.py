from django.shortcuts import render, redirect
from django.views import View
from .forms import ManagementForm
from User.staff_management import clean_and_create_data
from User.models import Position
from Period.models import Period
from Question.models import Survey, Question


def get_user_categories(user_id):
    user_categories = Position.objects.filter(user_id=user_id).values_list('category__name', flat=True)
    period_categories = Period.get_current_period().categories.values_list('name', flat=True)
    return set(user_categories).intersection(period_categories)


def get_questions(user_surveys, period):
    type_of_surveys = user_surveys.values_list('type', flat=True)
    period_questions = Question.objects.filter(period=period)
    if '2' in type_of_surveys:
        return period_questions.filter(type='2')
    elif '3' in type_of_surveys:
        return period_questions.filter(type='3') | period_questions.filter(category=user_surveys[0].respondent_position.category)
    elif '0' in type_of_surveys:
        return period_questions.filter(type='0')
    elif '1' in type_of_surveys:
        return period_questions.filter(type='1')
    return []


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
    def get(self, request, category):
        if not self.request.user.is_authenticated:
            return redirect('auth/login')
        current_period = Period.get_current_period()
        categories = get_user_categories(self.request.user.id)
        category = category if category in categories else None
        user_position = Position.objects.get(user_id=self.request.user.id, category__name=category) if category else None
        user_surveys = Survey.objects.filter(period=current_period, respondent_position=user_position, is_done=False)
        questions = get_questions(user_surveys, user_position)
        type_of_questions = questions.first().type
        context = {
            'categories': categories,
            'current_category': category,
            'position': user_position,
            'type_of_questions': type_of_questions,
            'serveys': user_surveys,
            'questions': questions,
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
            return render(request, 'Playground/admin.html', {'form': form, 'status': False, 'message': 'بدلیل خطا، بارگزاری فایل متوقف شد. لطفا مجددا تلاش کنید.'})
        return render(request, 'Playground/admin.html', {'form': form, 'status': True, 'message': 'داده‌ها با موفقیت بارگزاری شدند.'})
        
            
