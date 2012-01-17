import logbook
from logbook.compat import redirect_logging
from logbook.ticketing import TicketingHandler
from djlogbook.ticketing import DjangoORMBackend
from djlogbook.handlers import DjangoMailHandler
from django.conf import settings


class DjLogbookMiddleware(object):
    _setup = False
    _processor = None

    def _setup_app_logging(self):
        redirect_logging()

        nhandler = logbook.NullHandler()
        nhandler.push_application()

        thandler = TicketingHandler(
            '',
            backend=DjangoORMBackend,
            level=logbook.INFO,
            bubble=True)
        thandler.push_application()

        recepients = [mail for _, mail in settings.ADMINS]
        mhandler = DjangoMailHandler(
            settings.DEFAULT_FROM_EMAIL,
            recepients,
            level=logbook.ERROR,
            bubble=True)
        mhandler.push_application()

    def process_request(self, request):
        if not self._setup:
            try:
                self._setup_app_logging()
            finally:
                self._setup = True

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
