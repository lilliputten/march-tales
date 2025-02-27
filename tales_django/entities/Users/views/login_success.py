from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render

from core.helpers.utils import debugObj
from core.logging import getDebugLogger
from tales_django.core.pages import get_common_context, get_favorites_list_context, get_tracks_list_context

# from django.utils.translation import ugettext as _

logger = getDebugLogger()


@login_required
def login_success(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('index')

    context = {
        **get_common_context(request),
        **get_favorites_list_context(request),
        **get_tracks_list_context(request),
    }

    debugData = {
        'request': request,
        'cookies': request.COOKIES.get('cookies'),
        'mobile_auth': request.COOKIES.get('mobile_auth'),
        'request.user': request.user,
        'context': context,
    }
    debugStr = debugObj(debugData)
    logger.info(f'login_success\n{debugStr}')

    return render(
        request=request,
        template_name='tales_django/login_success.html.django',
        context=context,
    )
