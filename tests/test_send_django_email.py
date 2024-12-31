# How to run:
# ```bash
# [poetry run] python manage.py shell < tests/test_send_django_email.py
# ```
from django.conf import settings
from django.core.mail import send_mail

result = send_mail(
    subject='Test',
    message='Hello there!',
    from_email=settings.EMAIL_HOST_USER,
    recipient_list=['lilliputten@yandex.ru'],
    fail_silently=False,
)
print('Result:', result)
