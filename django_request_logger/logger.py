import logging

from . import middleware


def add_filter_to_all_handlers():
    filter = AddDjangoRequestFilter()
    for handler in logging._handlers.values():
        print("handler", handler)
        handler.addFilter(filter)


def get_client_ip(request):
    if request is None:
        return ""

    client_ip = request.META.get('REMOTE_ADDR')
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        client_ip += " [%s]" % request.META['HTTP_X_FORWARDED_FOR']
    return client_ip


class AddDjangoRequestFilter(object):
    def filter(self, record):
        # Initialise custom fields to empty, so the formatter doesn't raise an error if there is no request or user
        record.client_ip = ""
        record.username = ""
        record.absolute_url = ""
        record.raw_post_data = ""

        request = middleware.get_request()
        if request is not None:
            record.client_ip = get_client_ip(request)
            record.absolute_url = request.build_absolute_uri()

            try:
                record.raw_post_data = request.body
            except Exception as e:
                 record.raw_post_data = '<ERROR: %s>' % e.message

            if 'AUTHENTICATE_UID' in request.META:
                record.username = request.META['AUTHENTICATE_UID']
            elif 'HTTP_X_AUTH_SUBJECT' in request.META:
                record.username = request.META['HTTP_X_AUTH_SUBJECT']
            else:
                record.username = '_'
        return 1
