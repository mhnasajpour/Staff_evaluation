from .forms import User_form, Question_form
from .models import TYPE_CHOICES, ANSWER_CHOICES, Survey
from .qa_management import get_user_categories, get_questions, calc_total_points, add_question_answer, is_allowed_to_skip_survey
from .survey_management import update_surveys, create_questions
from Period.models import Period
from User.models import Position
from User.staff_management import update_staffs
from django.db.models import Sum
from django.http.response import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import json
from datetime import date


class Home(View):
    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('user:login')
        if self.request.user.is_superuser:
            return redirect('survey:management')
        category = get_user_categories(self.request.user.pk)
        if category:
            return redirect('survey:question_answers', category=category.pop())
        else:
            return render(request, 'Survey/question-answers.html')


class Question_answers(View):
    def get(self, request, category):
        if not self.request.user.is_authenticated:
            return redirect('user:login')
        current_period = Period.get_current_period()
        categories = get_user_categories(self.request.user.pk)
        category = category if category in categories else None
        user_position = Position.objects.get(user_id=self.request.user.pk, category__name=category) if category else None
        user_surveys, questions = get_questions(current_period, user_position)
        selected_survey = user_surveys[0] if user_surveys else None
        if request.GET.get('target'):
            selected_survey = get_object_or_404(user_surveys, pk=request.GET.get('target'))
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
            'choices': list(map(lambda choice: (choice[0] / 4, choice[0], choice[1]), ANSWER_CHOICES))[::-1],
            'allow_to_skip_survey': is_allowed_to_skip_survey(self.request.user.pk, category)
        }
        return render(request, 'Survey/question-answers.html', context=context)
    
    def post(self, request, category):
        if not self.request.user.is_authenticated:
            return redirect('user:login')
        try:
            info = json.loads(request.body.decode('utf-8'))
            current_period = Period.get_current_period()
            user_position = Position.objects.get(user_id=self.request.user.pk, category__name=category)
            selected_surveys, questions = get_questions(period=current_period, position=user_position)
            if int(info['survey']) not in selected_surveys.values_list('pk', flat=True):
                return JsonResponse({"message": 'اطلاعات سربرگ پرسشنامه نادرست است. لطفا صفحه را رفرش کنید و مجددا آن را پر کنید', "status": False}) 
            if len(info['points']) != questions.count():
                return JsonResponse({"message": 'همه سوالات پرسشنامه باید تکمیل شوند. لطفا مجددا آن را ارسال کنید.', "status": False}) 
            total_points = calc_total_points(questions, info['points'])
            if total_points < 10:
                return JsonResponse({"message": 'مجموع نمرات ثبت شده نباید کمتر از 10 باشد.', "status": False})
            if total_points > 90:
                return JsonResponse({"message": 'مجموع نمرات ثبت شده نباید بیشتر از 90 باشد.', "status": False})
            add_question_answer(info['survey'], questions, info['points'])
            return JsonResponse({"message": 'پرسشنامه با موفقیت ثبت شد.', "status": True})
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'بدلیل وجود خطا، پرسشنامه ثبت نشد. لطفا مجددا آن‌ را ارسال کنید.', 'status': False})


class Skip_surveys(View):
    def get(self, request, category):
        if not self.request.user.is_authenticated:
            return redirect('user:login')
        is_allowed_to_skip_survey(self.request.user.pk, category, do_skip=True)
        return redirect('survey:question_answers', category=category)


class Renew_surveys(View):
    def get(self, request):
        if not (self.request.user.is_authenticated and self.request.user.is_superuser):
            raise Http404()
        current_period = Period.get_current_period()
        if not current_period:
            return render(request, 'Survey/admin.html', {'user_form': User_form(), 'question_form': Question_form(), 'status': False, 'message': 'هیچ دوره زمانی ارزشیابی فعالی وجود ندارد. لطفا ابتدا دوره ارزشیابی تعریف کنید'})
        try:
            update_surveys(current_period)
            return render(request, 'Survey/admin.html', {'user_form': User_form(), 'question_form': Question_form(), 'status': True, 'message': 'پرسشنامه‌ها با موفقیت ایجاد شدند.'})
        except:
            return render(request, 'Survey/admin.html', {'user_form': User_form(), 'question_form': Question_form(), 'status': False, 'message': 'بدلیل وجود خطا، پرسشنامه‌ها ایجاد نشدند. لطفا مجددا تلاش کنید.'})


class Management(View):
    def get(self, request):
        if not (self.request.user.is_authenticated and self.request.user.is_superuser):
            raise Http404()
        return render(request, 'Survey/admin.html', {'user_form': User_form(), 'question_form': Question_form()})

    def post(self, request):
        if not (self.request.user.is_authenticated and self.request.user.is_superuser):
            raise Http404()
        try:
            if request.GET.get('type') == 'users' and request.FILES['user_file']:
                update_staffs(request.FILES['user_file'])
            if request.GET.get('type') == 'questions' and request.FILES['question_file']:
                create_questions(request.FILES['question_file'])
        except Exception as e:
            print(e)
            return render(request, 'Survey/admin.html', {'user_form': User_form(), 'question_form': Question_form(), 'status': False, 'message': 'بدلیل خطا، بارگذاری فایل متوقف شد. لطفا مجددا تلاش کنید.'})
        return render(request, 'Survey/admin.html', {'user_form': User_form(), 'question_form': Question_form(), 'status': True, 'message': 'داده‌ها با موفقیت بارگذاری شدند.'})