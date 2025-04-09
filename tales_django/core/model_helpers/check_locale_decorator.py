from functools import wraps

from django.conf import settings
from django.http import HttpRequest, HttpResponse

from .check_required_locale import check_required_locale


def check_locale_decorator(view_func):
    @wraps(view_func)
    def wrap(request: HttpRequest, *args, **kwargs):

        required_locale = check_required_locale(request)

        response: HttpResponse = view_func(request, *args, **kwargs)

        if required_locale:
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME,
                required_locale,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                domain=settings.LANGUAGE_COOKIE_DOMAIN,
                secure=settings.LANGUAGE_COOKIE_SECURE,
                httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
                samesite=settings.LANGUAGE_COOKIE_SAMESITE,
            )

        return response

    return wrap
