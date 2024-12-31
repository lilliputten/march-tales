from django.shortcuts import redirect
from django.contrib.auth import logout


def logoutUserRoute(request):
    logout(request)
    return redirect('index')


__all__ = []
