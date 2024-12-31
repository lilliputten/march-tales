import traceback

from django.test import TestCase
from django.core import mail

# @see https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Testing


class Test_user(TestCase):
    def test_send_email(self):
        try:
            """
            Sending email
            """
            connection = mail.get_connection(fail_silently=False)
            print('test_send_email: connection:' + str(connection))
            email = mail.EmailMessage(
                'Hello',
                'World',
                to=['lilliputten@gmail.com'],
                connection=connection,
            )
            print('test_send_email: email:' + str(email))
            result = email.send(fail_silently=False)
            print('test_send_email: result:' + repr(result))
            self.assertTrue(result)
        except Exception as err:
            errText = repr(err, show_stacktrace=False)
            sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
            errMsg = 'Error sending an email: ' + errText
            print('test_send_email: Traceback for the following error:' + sTraceback)
            print('test_send_email: ' + errMsg)
        finally:
            print('test_send_email: Finished')
