from django.http import HttpRequest
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from tales_django.core.pages import get_core_app_context


def privacy_policy_view(request: HttpRequest):
    return render(
        request=request,
        template_name='tales_django/privacy-policy.html.django',
        context=get_core_app_context(request),
    )


__all__ = ['privacy_policy_view']
