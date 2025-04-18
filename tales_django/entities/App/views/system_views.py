from django.contrib.sites.models import Site
from django.shortcuts import render
from django.views.generic import TemplateView

from tales_django.core.model_helpers import check_locale_decorator, check_required_locale


class RobotsView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'

    def get_context_data(self, **kwargs):
        context = super(RobotsView, self).get_context_data(**kwargs)
        site = Site.objects.get_current()
        context['site'] = site
        scheme = 'https' if self.request.is_secure() else 'http'
        context['scheme'] = scheme
        return context


# Error pages...


@check_locale_decorator
def page403(request, *args, **argv):
    return render(request, '403.html.django', {}, status=403)


@check_locale_decorator
def page404(request, *args, **argv):
    return render(request, '404.html.django', {}, status=404)


@check_locale_decorator
def page500(request, *args, **argv):
    return render(request, '500.html.django', {}, status=500)


__all__ = [
    'RobotsView',
    'page403',
    'page404',
    'page500',
]
