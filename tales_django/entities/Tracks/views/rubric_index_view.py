from django.http import HttpRequest
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from tales_django.core.pages import get_favorites_list_context, get_rubrics_list_context, get_common_context


def rubric_index_view(request: HttpRequest):
    context = {
        **get_common_context(request),
        **get_favorites_list_context(request),
        **get_rubrics_list_context(request),
    }

    return render(
        request=request,
        template_name='tales_django/rubric_index.html.django',
        context=context,
    )


__all__ = ['rubric_index_view']
