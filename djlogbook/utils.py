class cached_property(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, type=None):
        if obj is None:
            return self

        obj.__dict__[self.func.__name__] = value = self.func(obj)
        return value


def setup_logbook(**kwargs):
    import logbook
    from logbook.ticketing import TicketingHandler
    from .ticketing import DjangoORMBackend

    null_handler = logbook.NullHandler()
    null_handler.push_application()

    ticketing_handler = TicketingHandler(
        '',
        backend=DjangoORMBackend,
        level=logbook.INFO,
        bubble=True)
    ticketing_handler.push_application()


def on_celery_task_failure(
    sender=None,
    task_id=None,
    exception=None,
    args=None,
    kwargs=None,
    traceback=None,
    einfo=None,
    **other_kwargs):
    import logbook
    logbook.exception(
        '%s' % exception,
        exc_info=(einfo.type, einfo.exception, einfo.tb),
        extra=dict(task_id=task_id, args=args, kwargs=kwargs))


def setup_celery_task_logger(logger=None, **kwargs):
    logger.propagate = 1
