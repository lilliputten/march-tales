from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render


def index(request: HttpRequest):
    # events = [obj for obj in Event.objects.filter(public=True) if obj.can_register]
    # if request.user:
    #     for event in events:
    #         event.registration = event.get_active_event_registration_for_user(request.user)

    return render(
        request=request,
        template_name='tales_django/index.html.django',
        context={
            'user': request.user,
            # 'events': events,
        },
    )


def components_demo(request: HttpRequest):
    return render(request, 'demo/components-demo.html.django')


__all__ = [
    'index',
    'profile',
    'components_demo',
]
