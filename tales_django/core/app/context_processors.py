# -*- coding:utf-8 -*-
from django.conf import settings
from django.contrib.sites.models import Site  # To access site properties


def common_values(request):
    """
    Provide the values to access from templates as `{{ settings.VARIABLE }}`.
    See in `PASS_VARIABLES` dictionary in the `tales_django/settings.py` module.
    """
    data = {}
    data['settings'] = settings.PASS_VARIABLES
    data['site'] = Site.objects.get_current()
    return data
