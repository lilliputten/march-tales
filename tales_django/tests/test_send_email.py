import traceback

from django.test import TestCase

# @see https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Testing

from django.core import mail
from django.conf import settings

from core.helpers.errors import errorToString


class Test_send_email(TestCase):
    def test_send_django_email(self):
        try:
            """
            Sending email

            Should emails be actually sent from tests?

            See independent tests in `/tests`:

            - `test_send_smtplib_email.py`
            - `tests/test_send_django_email.py`
            """
            result = mail.send_mail(
                subject='Hello',
                message='Test',
                from_email=settings.EMAIL_HOST_USER,
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
