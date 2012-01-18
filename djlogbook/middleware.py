import logbook


class DjLogbookMiddleware(object):
    _processor = None

    def process_request(self, request):
        def inject_info(record):
            record.extra.update(
                ip=request.META.get('REMOTE_ADDR'),
                method=request.method,
                absolute_uri=request.build_absolute_uri(),
            )

        self._processor = logbook.Processor(inject_info)
        self._processor.push_application()

    def process_response(self, request, response):
        self._processor.pop_application()
        return response
