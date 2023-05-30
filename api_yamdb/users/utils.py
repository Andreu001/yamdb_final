import re

from django.conf import settings
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError
from users.models import User


def username_validate(name):
    """Проверка имени пользователя"""
    regex = re.compile(r'^[\w.@+-]+')
    if not regex.match(name):
        raise ValidationError('Не допустимые символы в имени')
    if name == 'me':
        raise ValidationError(
            'me не может быть использовано в качестве имени пользоателя'
        )
    if name is None or name == "":
        raise ValidationError(
            'имя не может быть пустым'
        )


def email_validate(value):
    """Проверка наличия такой почты в БД"""
    if User.objects.filter(email=value):
        raise ValidationError('Такая почта уже зарегистрирована в БД')


def sent_email_with_confirmation_code(to_email, code):
    """Отправка сообщения пользователю с кодом подтверждения"""
    subject = 'Отвчать на это письмо не нужно'
    message = (
        f'Ваш код подтверждения для регистрации: {code} '
        f'Вам необходимо отправить запрос /api/v1/auth/token/'
        f'В запросе передайте username и confirmation_code'
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [to_email])
