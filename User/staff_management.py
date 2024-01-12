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
    'category_id': 'رسته',
    'category': 'عنوان رسته',
}


def remove_all_users():
    User.objects.filter(is_staff=False).delete()


def remove_all_categories():
    Category.objects.all().delete()


def remove_all_positions():
    Position.objects.all().delete()


def add_categories(categories):
    for category in categories:
        new_category = Category()
        new_category.name = category
        new_category.save()


def add_users(users):
    national_codes = set()
    for user in users.iterrows():
        new_user = User()
        if user[1][header['national_code']] in national_codes:
            continue
        new_user.set_password(str(user[1][header['national_code']]))
        new_user.username = user[1][header['personnel_code']]
        new_user.first_name = user[1][header['first_name']]
        new_user.last_name = user[1][header['last_name']]
        new_user.personnel_code = user[1][header['personnel_code']]
        new_user.national_code = user[1][header['national_code']]
        national_codes.add(user[1][header['national_code']])
        new_user.save()


def add_positions(positions):
    for position in positions.iterrows():
        new_position = Position()
        new_position.title = position[1][header['position_title']]
        new_position.unit = position[1][header['organizational_unit']]

        user = User.objects.get(
            personnel_code=position[1][header['personnel_code']])
        new_position.user = user

        if position[1][header['manager_personnel_code']] > 0:
            manager = User.objects.get(
                personnel_code=position[1][header['manager_personnel_code']])
            new_position.manager = manager

        category = Category.objects.get(name=position[1][header['category']])
        new_position.category = category

        new_position.save()


def clean_and_create_data(file):
    remove_all_categories()
    remove_all_positions()
    remove_all_users()

    data = pd.read_excel(file)
    add_categories(data[header['category']].unique())
    add_users(data)
    add_positions(data)
