from django.http import HttpRequest
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy

from tales_django.models import Rubric


def index_view(request: HttpRequest):
    # events = [obj for obj in Event.objects.filter(public=True) if obj.can_register]
    # if request.user:
    #     for event in events:
    #         event.registration = event.get_active_event_registration_for_user(request.user)

    count = 21
    plural_test = ngettext_lazy('there is %(count)d object', 'there are %(count)d objects', count,) % {
        'count': count,
    }
    rubrics = Rubric.objects.all()
    return render(
        request=request,
        template_name='tales_django/index.html.django',
        context={
            'user': request.user,
            'rubrics': rubrics,
            # 'events': events,
            # Translators: The sample translation string
            'sample_text': _('Sample Message'),
            'plural_test': plural_test,
        },
    )


__all__ = ['index_view']
