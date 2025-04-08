from django.http import HttpRequest
from django.shortcuts import render

from tales_django.core.model_helpers import check_locale_decorator
from tales_django.core.pages import (get_common_context,
                                     get_favorites_list_context,
                                     get_tags_list_context)


@check_locale_decorator
def tag_index_view(request: HttpRequest):
    context = {
        **get_common_context(request),
        **get_favorites_list_context(request),
        **get_tags_list_context(request),
    }

    return render(
        request=request,
        template_name='tales_django/tag_index.html.django',
        context=context,
    )


__all__ = ['tag_index_view']
