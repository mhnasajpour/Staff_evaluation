import pandas as pd
from .models import User, Category, Position

header = {
    'first_name': 'نام',
    'last_name': 'نام خانوادگي',
    'position_title': 'عنوان سمت',
    'organizational_unit': 'واحد سازماني',
    'personnel_code': 'كد پرسنلي',
    'national_code': 'كد ملي',
    'manager_personnel_code': 'كد پرسنلي مدير',
    'category': 'عنوان رسته',
}


def deactivate_all_positions():
    Position.objects.all().update(is_active=False)


def update_categories(categories):
    for category_name in categories:
        Category.objects.get_or_create(name=category_name)


def update_users(users):
    personnel_codes = list(User.objects.values_list('personnel_code', flat=True))
    for user in users.iterrows():
        new_user = User()
        if user[1][header['personnel_code']] in personnel_codes:
            continue
        new_user.set_password(str(user[1][header['national_code']]))
        new_user.username = user[1][header['personnel_code']]
        new_user.first_name = user[1][header['first_name']]
        new_user.last_name = user[1][header['last_name']]
        new_user.personnel_code = user[1][header['personnel_code']]
        new_user.national_code = user[1][header['national_code']]
        personnel_codes.append(user[1][header['national_code']])
        new_user.save()


def update_positions(positions):
    for position in positions.iterrows():
        new_position = None
        if position[1][header['manager_personnel_code']] > 0:
            new_position = Position.objects.get_or_create(
                user_id=position[1][header['personnel_code']],
                manager_id=position[1][header['manager_personnel_code']],
                category=Category.objects.get(name=position[1][header['category']]))
        else:
            new_position = Position.objects.get_or_create(
                user_id=position[1][header['personnel_code']],
                category=Category.objects.get(name=position[1][header['category']]))
        new_position[0].title = position[1][header['position_title']]
        new_position[0].unit = position[1][header['organizational_unit']]
        new_position[0].is_active = True
        new_position[0].save()

        

def update_staffs(file):
    data = pd.read_excel(file)
    deactivate_all_positions()
    update_categories(data[header['category']].unique())
    update_users(data)
    update_positions(data)
