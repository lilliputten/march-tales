from django.http import HttpRequest
from django.utils import translation
from django.conf import settings

from core.logging import getDebugLogger

from .get_valid_language import get_valid_language

# from django.conf import settings
# from core.helpers.utils import debugObj

logger = getDebugLogger()


def _get_required_locale(request: HttpRequest):
    hl_locale = str(request.GET.get('hl', ''))
    if hl_locale is not None and hl_locale:
        return hl_locale
    # # !!!
    language_cookie = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
    accept_language = get_valid_language(request.headers.get('Accept-Language'))  # current_language
    if language_cookie is None and accept_language is not None and accept_language:
        return accept_language
    return ''


def check_required_locale(request: HttpRequest):
    """
    Fetch and set language from telegram request and set it for the response.
    """

    # current_language = request.LANGUAGE_CODE
    current_language = translation.get_language()
    set_language = False
    required_locale = _get_required_locale(request)
    if required_locale is not None and required_locale and required_locale != current_language:
        required_locale = get_valid_language(required_locale)
        set_language = True
    # # TODO: Find out the telegram language parameter.
    # debugData = {
    #     'required_locale': required_locale,
    #     'current_language': current_language,
    #     'set_language': set_language,
    #     'LANGUAGE_COOKIE_NAME': settings.LANGUAGE_COOKIE_NAME,
    #     'headers': '\n' + debugObj(request.headers),
    #     'cookies': '\n' + debugObj(request.COOKIES),
    # }
    # debugStr = debugObj(debugData)
    # logger.info(f'track_details_view: Check language\n{debugStr}')
    if set_language:
        translation.activate(required_locale)
        return required_locale


__all__ = [
    'check_required_locale',
]
