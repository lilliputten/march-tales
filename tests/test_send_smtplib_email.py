import os
import sys
import pathlib
import traceback
import smtplib

# Inject project path to allow server-side tests
sys.path.insert(1, pathlib.Path(os.getcwd()).as_posix())

from core.helpers.errors import errorToString
from core.djangoConfig import (
    EMAIL_HOST,
    EMAIL_PORT,
    DEFAULT_FROM_EMAIL,
    EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD,
    # EMAIL_USE_TLS,
    # EMAIL_USE_SSL,
)

def test_send_smtplib_email():
    try:
        """
        Sending email
        """
        print(f'test_send_smtplib_email: Starting with EMAIL_HOST={EMAIL_HOST}...')
        conn = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=5)
        print('test_send_smtplib_email: conn:', repr(conn))
        conn.ehlo()
        conn.starttls()
        # conn.login('goldenjeru', 'gmail_pwd') # SMTPAuthenticationError(535, b'Incorrect authentication data')
        conn.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        mailBody = f"""
From: {DEFAULT_FROM_EMAIL}
To: dmia@yandex.ru
Subject: Test msg
Content-Type: text/plain; charset="UTF-8";

Hello again, darling!
        """.strip()
        errs = conn.sendmail(DEFAULT_FROM_EMAIL, 'dmia@yandex.ru', mailBody)
        result = len(errs) == 0
        print(f'test_send_smtplib_email: Finished ({result}): {errs}')
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error sending an email: ' + errText
        print('test_send_smtplib_email: Traceback for the following error:' + sTraceback)
        print('test_send_smtplib_email: ' + errMsg)


test_send_smtplib_email()
