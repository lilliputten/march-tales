from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render


@login_required
def profile(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('index')
    return render(
        request=request,
        template_name='tales_django/profile.html.django',
        context={
            # 'active_regs': Registration.active_for_user(request.user),
            'user': request.user,
        },
    )
