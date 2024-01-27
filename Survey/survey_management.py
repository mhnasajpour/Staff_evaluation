import random
from User.models import Position
from .models import Survey

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
    positions = Position.objects.filter(category__is_root=False, category__name__in=allowed_categories)
    for position in positions:
        Survey.objects.create(period=period, target_position=position, respondent_position=position, type='0')


def create_manager_assessment_surveys(period):
    allowed_categories = period.categories.values_list('name', flat=True)
    positions = Position.objects.filter(category__name__in=allowed_categories)
    for position in positions:
        manager_positions = Position.objects.filter(user=position.manager)
        if manager_positions:
            Survey.objects.create(period=period, target_position=position, respondent_position=manager_positions[0], type='1')


def create_colleague_assessment_surveys(period):
    allowed_categories = period.categories.values_list('name', flat=True)
    positions = Position.objects.filter(category__is_root=False, category__name__in=allowed_categories)
    for position in positions:
        colleagues = Position.objects.exclude(user=position.user).filter(manager=position.manager, category=position.category)
        random_colleagues = random.sample(list(colleagues), k=3 if colleagues.count() > 3 else colleagues.count())
        for target_position in random_colleagues:
            Survey.objects.create(period=period, target_position=target_position, respondent_position=position, type='2')


def create_same_category_assessment_surveys(period):
    allowed_categories = period.categories.values_list('name', flat=True)
    positions = Position.objects.filter(category__is_root=False, category__name__in=allowed_categories)
    for position in positions:
        same_category = Position.objects.exclude(user=position.user).filter(category=position.category)
        random_same_category = random.sample(list(same_category), k=3 if same_category.count() > 3 else same_category.count())
        for target_position in random_same_category:
            Survey.objects.create(period=period, target_position=target_position, respondent_position=position, type='3')