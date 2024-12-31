import traceback

from django.test import TestCase

# @see https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Testing

from django.core import mail

# from tales_django.core.app.backends import EmailBackend
from django.core.mail.backends.locmem import EmailBackend

from core.helpers.errors import errorToString

from django.conf import settings


from core.helpers.errors import errorToString
from core.djangoConfig import (
    EMAIL_HOST,
    EMAIL_PORT,
    DEFAULT_FROM_EMAIL,
    EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD,
    EMAIL_USE_TLS,
    EMAIL_USE_SSL,
)

# settings.configure(
#     EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
#     EMAIL_HOST=EMAIL_HOST,
#     EMAIL_PORT=EMAIL_PORT,
#     EMAIL_USE_SSL=EMAIL_USE_SSL,
#     EMAIL_HOST_USER=EMAIL_HOST_USER,
#     EMAIL_HOST_PASSWORD=EMAIL_HOST_PASSWORD,
#     DEFAULT_FROM_EMAIL=DEFAULT_FROM_EMAIL,
# )


class Test_send_email(TestCase):
    def test_send_django_email(self):
        try:
            """
            Sending email
            """
            print(f'test_send_django_email: Starting with EMAIL_HOST={EMAIL_HOST}...')
            print('settings.EMAIL_BACKEND:', settings.EMAIL_BACKEND),
            print('settings.EMAIL_HOST:', settings.EMAIL_HOST),
            print('settings.EMAIL_PORT:', settings.EMAIL_PORT),
            print('settings.EMAIL_USE_TLS:', settings.EMAIL_USE_TLS),
            print('settings.EMAIL_USE_SSL:', settings.EMAIL_USE_SSL),
            print('settings.DEFAULT_FROM_EMAIL:', settings.DEFAULT_FROM_EMAIL),
            print('settings.EMAIL_HOST_USER:', settings.EMAIL_HOST_USER),
            print('settings.EMAIL_HOST_PASSWORD:', settings.EMAIL_HOST_PASSWORD),
            conn: EmailBackend = mail.get_connection(fail_silently=False)
            print('test_send_django_email: connection:' + str(conn))
            # email = mail.EmailMessage(
            #     'Hello',
            #     'From Django',
            #     to=['dmia@yandex.ru'],
            #     connection=conn,
            # )
            # print('test_send_django_email: email:' + str(email))
            # result = email.send(fail_silently=False)
            result = mail.send_mail(
                subject='Hello',
                message='Test',
                from_email=EMAIL_HOST_USER,
                recipient_list=['lilliputten@gmail.com'],
                fail_silently=False,
            )
            print('test_send_django_email: result:' + repr(result))
            self.assertTrue(result)
        except Exception as err:
            errText = errorToString(err, show_stacktrace=False)
            sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
            errMsg = 'Error sending an email: ' + errText
            print('test_send_django_email: Traceback for the following error:' + sTraceback)
            print('test_send_django_email: ' + errMsg)
        finally:
            print('test_send_django_email: Finished')
