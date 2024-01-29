import pandas as pd
import random
from Period.models import Period
from User.models import Category, Position
from .models import TYPE_CHOICES, Survey, QuestionGroup, Question


header = {
    'group': 'گروه',
    'content': 'سوال',
    'weight': 'وزن',
    'type': 'نوع',
    'category': 'رسته'
}


def remove_all_surveys(period):
    Survey.objects.all().filter(period=period).delete()


def update_surveys(period):
    remove_all_surveys(period)
    create_self_assessment_surveys(period)
    create_manager_assessment_surveys(period)
    create_colleague_assessment_surveys(period)
    create_same_category_assessment_surveys(period)


def create_self_assessment_surveys(period):
    allowed_categories = period.categories.values_list('name', flat=True)
    positions = Position.objects.filter(is_active=True, category__is_root=False, category__name__in=allowed_categories)
    for position in positions:
        Survey.objects.create(period=period, target_position=position, respondent_position=position, type='0')


def create_manager_assessment_surveys(period):
    allowed_categories = period.categories.values_list('name', flat=True)
    positions = Position.objects.filter(is_active=True, category__name__in=allowed_categories)
    for position in positions:
        manager_positions = Position.objects.filter(is_active=True, user=position.manager)
        if manager_positions:
            Survey.objects.create(period=period, target_position=position, respondent_position=manager_positions[0], type='2')
            Survey.objects.create(period=period, target_position=manager_positions[0], respondent_position=position, type='1')


def create_colleague_assessment_surveys(period):
    allowed_categories = period.categories.values_list('name', flat=True)
    positions = Position.objects.filter(is_active=True, category__is_root=False, category__name__in=allowed_categories)
    for position in positions:
        colleagues = Position.objects.exclude(user=position.user).filter(is_active=True, manager=position.manager, category=position.category)
        random_colleagues = random.sample(list(colleagues), k=3 if colleagues.count() > 3 else colleagues.count())
        for target_position in random_colleagues:
            Survey.objects.create(period=period, target_position=target_position, respondent_position=position, type='3')


def create_same_category_assessment_surveys(period):
    allowed_categories = period.categories.values_list('name', flat=True)
    positions = Position.objects.filter(is_active=True, category__is_root=False, category__name__in=allowed_categories)
    for position in positions:
        same_category = Position.objects.exclude(user=position.user).filter(is_active=True, category=position.category)
        random_same_category = random.sample(list(same_category), k=3 if same_category.count() > 3 else same_category.count())
        for target_position in random_same_category:
            Survey.objects.create(period=period, target_position=target_position, respondent_position=position, type='4')


def remove_current_period_questions():
    Question.objects.filter(period=Period.get_current_period()).delete()


def create_current_period_questions(questions):
    for question in questions.iterrows():
        new_question = Question()
        new_question.group = QuestionGroup.objects.get_or_create(name=question[1][header['group']])[0]
        new_question.content = question[1][header['content']]
        new_question.period = Period.get_current_period()
        if str(question[1][header['weight']]) != 'nan':
            new_question.weight = question[1][header['weight']]
        new_question.type = list(map(lambda obj: obj[1], TYPE_CHOICES)).index(question[1][header['type']])
        if str(question[1][header['category']]) != 'nan':
            new_question.category = Category.objects.get_or_create(name=question[1][header['category']])[0]
        new_question.save()


def create_questions(file):
    data = pd.read_excel(file)
    remove_current_period_questions()
    create_current_period_questions(data)
