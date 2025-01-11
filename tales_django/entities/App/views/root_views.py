from django.http import HttpRequest
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

# from django.utils.translation import ngettext_lazy


def empty_demo(request: HttpRequest):
    return render(request, 'demo/empty-demo.html.django')


def components_demo(request: HttpRequest):
    return render(request, 'demo/components-demo.html.django')


__all__ = [
    # 'index',
    'profile',
    'components_demo',
    'empty_demo',
]
