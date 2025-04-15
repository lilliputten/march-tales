from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_user_route(request):
    logout(request)
    return redirect('logged_out')


__all__ = []
