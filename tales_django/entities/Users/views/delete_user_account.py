import traceback

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect
from django.contrib.auth import logout


from core.helpers.errors import errorToString
from core.logging import getDebugLogger


logger = getDebugLogger()


@login_required
def delete_user_account(request: HttpRequest):
    try:
        user = request.user
        user.session_set.all().delete()
        user.delete()
        logout(request)
        messages.success(request, 'Your account has been removed successfully')
        return redirect('login')
    except Exception as err:
        sError = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        debug_data = {
            'err': err,
            'traceback': sTraceback,
        }
        logger.error('Caught error %s (re-raising): %s', sError, debug_data)
        raise err