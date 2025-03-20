from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.utils.translation import activate

from core.helpers.utils import debugObj
from core.logging import getDebugLogger
from tales_django.core.model_helpers import get_valid_language
from tales_django.core.pages import get_common_context, get_favorites_list_context, get_tracks_list_context
from tales_django.entities.Tracks.models import Track


logger = getDebugLogger()


def track_details_view(request: HttpRequest, track_id):

    # # TODO: Fetch and set language from telegram request and set it for the response. Find telegram language parameter.
    # current_language = request.LANGUAGE_CODE
    # required_locale = get_valid_language(request.headers.get('Accept-Language'))   # current_language
    # set_language = False
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
    # if set_language:
    #     activate(required_locale)

    track = get_object_or_404(Track, id=track_id)

    context = {
        **get_common_context(request),
        **get_tracks_list_context(request),
        **get_favorites_list_context(request),
        'track_id': track_id,
        'track': track,
    }

    response = render(
        request=request,
        template_name='tales_django/track_details.html.django',
        context=context,
    )

    # # Set language cookie, from `set_language(request)`:
    # if set_language:
    #     response.set_cookie(
    #         settings.LANGUAGE_COOKIE_NAME,
    #         required_locale,
    #         max_age=settings.LANGUAGE_COOKIE_AGE,
    #         path=settings.LANGUAGE_COOKIE_PATH,
    #         domain=settings.LANGUAGE_COOKIE_DOMAIN,
    #         secure=settings.LANGUAGE_COOKIE_SECURE,
    #         httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
    #         samesite=settings.LANGUAGE_COOKIE_SAMESITE,
    #     )

    return response


__all__ = ['track_details_view']
