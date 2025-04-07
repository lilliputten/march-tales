from django.http import HttpRequest
from django.utils.translation import activate

from core.logging import getDebugLogger

from .get_valid_language import get_valid_language

# from django.conf import settings
# from core.helpers.utils import debugObj

logger = getDebugLogger()


def _get_required_locale(request: HttpRequest):
    hl_locale = str(request.GET.get('hl', ''))
    if hl_locale is not None and hl_locale:
        return hl_locale
    required_locale = get_valid_language(request.headers.get('Accept-Language'))  # current_language
    if required_locale is not None and required_locale:
        return required_locale
    return ''


def check_required_locale(request: HttpRequest):
    """
    Fetch and set language from telegram request and set it for the response.
    """

    current_language = request.LANGUAGE_CODE
    required_locale = _get_required_locale(request)
    required_locale = get_valid_language(required_locale)
    set_language = required_locale != current_language
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
        activate(required_locale)


__all__ = [
    'check_required_locale',
]
