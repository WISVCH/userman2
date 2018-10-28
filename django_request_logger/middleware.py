import threading


_thread_local = threading.local()


def get_request():
    return getattr(_thread_local, 'current_django_request', None)


def _set_request(value):
    _thread_local.current_django_request = value


class StoreRequestMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        _set_request(request)
        return self.get_response(request)

