from django.shortcuts import render, redirect
from django.views import View
from .forms import ManagementForm
from User.staff_management import clean_and_create_data
from User.models import Position
from Period.models import Period
from Question.models import TYPE_CHOICES, ANSWER_CHOICES, Survey, Question
from django.shortcuts import get_object_or_404
from django.db.models import Sum



def get_user_categories(user_id):
    user_categories = Position.objects.filter(user_id=user_id).values_list('category__name', flat=True)
    period_categories = Period.get_current_period().categories.values_list('name', flat=True)
    return set(user_categories).intersection(period_categories)


def get_questions(period, position):
    user_surveys = Survey.objects.filter(period=period, respondent_position=position, is_done=False)
    type_of_surveys = user_surveys.values_list('type', flat=True)
    period_of_questions = Question.objects.filter(period=period)
    selected_surveys, questions = user_surveys.none(), period_of_questions.none() 
    if '2' in type_of_surveys:
        selected_surveys = user_surveys.filter(type='2')
        questions = period_of_questions.filter(type='2')
    elif '3' in type_of_surveys:
        selected_surveys = user_surveys.filter(type='3')
        questions = period_of_questions.filter(type='3') | period_of_questions.filter(category=user_surveys[0].respondent_position.category)
    elif '0' in type_of_surveys:
        selected_surveys = user_surveys.filter(type='0')
        questions = period_of_questions.filter(type='0')
    elif '1' in type_of_surveys:
        selected_surveys = user_surveys.filter(type='1')
        questions = period_of_questions.filter(type='1')
    return selected_surveys, questions


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
        user_surveys, questions = get_questions(current_period, user_position)
        selected_survey = user_surveys[0] if user_surveys else None
        if request.GET.get('target'):
            selected_survey = get_object_or_404(user_surveys, id=request.GET.get('target'))
        type_of_questions = TYPE_CHOICES[int(questions.first().type)][1] if questions else None
        context = {
            'categories': categories,
            'current_category': category,
            'position': user_position,
            'type_of_questions': type_of_questions,
            'surveys': user_surveys,
            'first_survey': selected_survey,
            'questions': questions,
            'total_points': questions.aggregate(Sum('weight'))['weight__sum'],
            'choices': list(map(lambda choice: (round(choice[0] / 3, 2), choice[1]), ANSWER_CHOICES))[::-1],
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
        
            
