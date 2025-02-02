from django.middleware.csrf import CsrfViewMiddleware

NOOP = lambda _: _


def check_csrf(request):
    reason = CsrfViewMiddleware(NOOP).process_view(request, None, (), {})
    # CSRF failed if reason returned
    return False if reason else True
