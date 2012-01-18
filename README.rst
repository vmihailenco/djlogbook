Djlogbook
=========

This is Django ORM backend for logbook ticketing functionality. It
also contains few utils to setup some default logging configuration,
but if you want complex logging you should write them yourself.

Typical setup
=============

settings.py::

    MIDDLEWARE_CLASSES = (
        'djlogbook.middleware.DjLogbookMiddleware',
        ...
    )


    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'logbook': {
                'level': 'DEBUG',
                'class': 'logbook.compat.RedirectLoggingHandler',
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            '': {
                'handlers': ['logbook'],
                'level': 'DEBUG',
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }

core/models.py or urls.py::

    from djlogbook.utils import setup_logbook
    setup_logbook()

Celery setup
============

settings.py::

    from celery import signals
    from djlogbook.utils import setup_celery_task_logger, on_celery_task_failure

    signals.setup_logging.connect(lambda **kwargs: True)
    signals.after_setup_task_logger.connect(setup_celery_task_logger)
    signals.task_failure.connect(on_celery_task_failure)
