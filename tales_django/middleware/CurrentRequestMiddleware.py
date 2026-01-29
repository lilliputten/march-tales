from threading import local

thread_data = local()


class CurrentRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        thread_data.request = request
        response = self.get_response(request)
        thread_data.request = None  # Clean up!
        return response


__all__ = [
    'thread_data',
    'CurrentRequestMiddleware',  # middleware class name should be unique to avoid conflicts in different apps or modules.
]
