from django.core.mail import send_mail
from django.conf import settings


def send_birthday_email(user):
    send_mail(
        subject='Happy birthday!',
        message='Поздравляем с Днем рождения и желаем успехов в учебе и личной жизни!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )
    # print(f'Сообщение отправлено {subscriber.user.email}')
