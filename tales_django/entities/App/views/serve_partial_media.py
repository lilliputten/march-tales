from django.contrib.staticfiles.views import serve
from rest_framework import status


def serve_partial_media(request, path, insecure=False, **kwargs):
    """
    Customize the response of serving static files.

    Note:
        This should only ever be used in development, and never in production.
    """
    response = serve(request, path, insecure=True)
    content_type = str(response.get('Content-Type', ''))
    if content_type.startswith('audio'):
        # response['Access-Control-Allow-Origin'] = '*'
        response.status_code = status.HTTP_206_PARTIAL_CONTENT
        response['Accept-Ranges'] = 'bytes'
        response['X-Accel-Buffering'] = 'no'
    # if path.endswith('sw.js'):
    #    response['Service-Worker-Allowed'] = '/'
    return response


__all__ = [
    'serve_partial_media',
]
