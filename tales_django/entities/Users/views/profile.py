from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render

from tales_django.core.pages import get_common_context, get_favorites_list_context, get_tracks_list_context

# from django.utils.translation import ugettext as _


@login_required
def profile(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('index')

    context = {
        **get_common_context(request),
        **get_tracks_list_context(request),
        **get_favorites_list_context(request),
    }

    return render(
        request=request,
        template_name='tales_django/profile.html.django',
        context=context,
    )
