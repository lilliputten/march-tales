from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render

from core.helpers.utils import debugObj
from core.logging import getDebugLogger
from tales_django.core.pages import (get_common_context,
                                     get_favorites_list_context,
                                     get_tracks_list_context)

# from django.utils.translation import ugettext as _

logger = getDebugLogger()


@login_required
def login_success(request: HttpRequest, key=''):
    if not request.user.is_authenticated:
        return redirect('index')

    session_key = request.session.session_key

    if not session_key:
        return redirect('index')

    mobile_auth = request.COOKIES.get('mobile_auth')

    context = {
        **get_common_context(request),
        **get_favorites_list_context(request),
        **get_tracks_list_context(request),
    }

    host = request.headers.get('Host')
    referer = request.headers.get('Referer')

    debugData = {
        'key': key,
        'session_key': session_key,
        'host': host,
        'referer': referer,
        'request': request,
        'cookies': request.COOKIES.get('cookies'),
        'mobile_auth': mobile_auth,
        'request.user': request.user,
        'context': context,
    }
    debugStr = debugObj(debugData)
    logger.info(f'login_success\n{debugStr}')

    if not key and mobile_auth:
        return redirect(f'/login-success/{session_key}/')

    response = render(
        request=request,
        template_name='tales_django/login_success.html.django',
        context=context,
    )
    response.set_cookie('TEST', 'TEST')
    return response
