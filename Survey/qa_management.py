from .models import Survey, Question, QuestionAnswer
from User.models import Position
from Period.models import Period
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
    if '3' in type_of_surveys:
        selected_surveys = user_surveys.filter(type='3')
        questions = period_of_questions.filter(type='3')
    elif '4' in type_of_surveys:
        selected_surveys = user_surveys.filter(type='4')
        questions = period_of_questions.filter(type='4') | period_of_questions.filter(category=user_surveys[0].respondent_position.category)
    elif '0' in type_of_surveys:
        selected_surveys = user_surveys.filter(type='0')
        questions = period_of_questions.filter(type='0')
    elif '1' in type_of_surveys:
        selected_surveys = user_surveys.filter(type='1')
        questions = period_of_questions.filter(type='1')
    elif '2' in type_of_surveys:
        selected_surveys = user_surveys.filter(type='2')
        questions = period_of_questions.filter(type='2')
    return selected_surveys, questions


def calc_total_points(questions, points):
    result = 0
    for index, question in enumerate(questions):
        result += question.weight * int(points[index]) / 4
    return result / questions.aggregate(Sum('weight'))['weight__sum'] * 100


def add_question_answer(survey, questions, points):
    for index, question in enumerate(questions):
        QuestionAnswer.objects.create(survey_id=survey, question=question, answer=int(points[index]))
        Survey.objects.filter(pk=survey).update(is_done=True)


def is_allowed_to_skip_survey(user_id, category, do_skip=False):
    period = Period.get_current_period()
    user_position = Position.objects.get(user_id=user_id, category__name=category)
    not_answered_survey, _ = get_questions(period=period, position=user_position)
    if not not_answered_survey:
        return False
    sample_survey = not_answered_survey.first()
    answered_survey = Survey.objects.filter(period=sample_survey.period, respondent_position=sample_survey.respondent_position, type=sample_survey.type, is_done=True)
    if (sample_survey.type == '0') or (sample_survey.type in ['3', '4'] and answered_survey):
        if do_skip:
            not_answered_survey.update(is_done=True)
        return True