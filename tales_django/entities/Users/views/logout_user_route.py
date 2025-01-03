from django.shortcuts import redirect
from django.contrib.auth import logout


def logout_user_route(request):
    logout(request)
    return redirect('index')


__all__ = []
