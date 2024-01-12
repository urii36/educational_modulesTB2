import datetime

from celery import shared_task
from users.models import User
from users.services import send_birthday_email


@shared_task
def check_birthday():
    users = User.objects.all()
    print(users)
    current_date = datetime.date.today()
    print(current_date)
    for user in users:
        if user.birth_date is not None:
            print(user.birth_date)
            print(user.birth_date.month)
            print(current_date.month)
            print(user.birth_date.day)
            print(current_date.day)
            if user.birth_date.month == current_date.month and user.birth_date.day == current_date.day:
                send_birthday_email(user)
