import logbook
from django.db import models
from django.utils import simplejson

from .utils import cached_property


class Ticket(models.Model):
    LEVEL_CHOICES = (
        (logbook.CRITICAL, 'CRITICAL'),
        (logbook.ERROR, 'ERROR'),
        (logbook.WARNING, 'WARNING'),
        (logbook.NOTICE, 'NOTICE'),
        (logbook.INFO, 'INFO'),
        (logbook.DEBUG, 'DEBUG'),
        (logbook.NOTSET, 'NOTSET'),
    )

    ticket_id = models.AutoField(primary_key=True)
    record_hash = models.CharField(max_length=40, unique=True, db_index=True)
    level = models.IntegerField(choices=LEVEL_CHOICES)
    channel = models.CharField(max_length=120)
    location = models.CharField(max_length=512)
    module = models.CharField(max_length=256)
    last_occurrence_time = models.DateTimeField(null=True, blank=True)
    occurrence_count = models.IntegerField(default=0)
    solved = models.BooleanField(default=False, db_index=True)
    app_id = models.CharField(max_length=80)

    class Meta:
        db_table = 'djlogbook_tickets'
        get_latest_by = 'last_occurrence_time'

    def __unicode__(self):
        return 'Ticket %s' % self.ticket_id


class Occurrence(models.Model):
    occurrence_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket)
    time = models.DateTimeField()
    data = models.TextField()
    app_id = models.CharField(max_length=80)

    class Meta:
        db_table = 'djlogbook_occurrences'
        get_latest_by = 'time'

    def __unicode__(self):
        return 'Occurrence %s' % self.occurrence_id

    @cached_property
    def _data(self):
        return simplejson.loads(self.data)

    @property
    def level(self):
        return int(self._data.get('level', logbook.NOTSET))

    @property
    def level_name(self):
        return dict(Ticket.LEVEL_CHOICES).get(self.level)

    @property
    def message(self):
        return self._data.get('message', '')

    @property
    def short_message(self):
        if len(self.message) > 32:
            return self.message[:32] + '...'
        else:
            return self.message

    @property
    def formatted_exception(self):
        return self._data.get('formatted_exception', '')
