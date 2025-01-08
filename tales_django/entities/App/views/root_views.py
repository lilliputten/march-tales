from django.http import HttpRequest
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy


def components_demo(request: HttpRequest):
    return render(request, 'demo/components-demo.html.django')


__all__ = [
    # 'index',
    'profile',
    'components_demo',
]
