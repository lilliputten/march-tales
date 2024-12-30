from django.shortcuts import redirect
from django.contrib.auth import logout


def logoutUser(request):
    logout(request)
    return redirect('index')


__all__ = []
