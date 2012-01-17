from logbook.ticketing import BackendBase
from django.db.models import F
from django.utils import simplejson

from .models import Ticket, Occurrence


class DjangoORMBackend(BackendBase):
    def setup_backend(self):
        """Setup the database backend."""
        pass

    def record_ticket(self, record, data, hash, app_id):
        """Records a log record as ticket."""
        ticket, _ = Ticket.objects.get_or_create(
            record_hash=hash,
            defaults=dict(
                level=record.level,
                channel=record.channel or u'',
                location=u'%s:%d' % (record.filename, record.lineno),
                module=record.module or u'<unknown>',
                app_id=app_id
            ))
        Occurrence.objects.create(
            ticket_id=ticket.ticket_id,
            time=record.time,
            app_id=app_id,
            data=simplejson.dumps(data))
        Ticket.objects \
            .filter(ticket_id=ticket.ticket_id) \
            .update(
                occurrence_count=F('occurrence_count') + 1,
                last_occurrence_time=record.time,
                solved=False)

    def count_tickets(self):
        """Returns the number of tickets."""
        return Ticket.objects.count()

    def get_tickets(
        self, order_by='-last_occurrence_time', limit=50, offset=0):
        """Selects tickets from the database."""
        return list(Ticket.objects.order_by(order_by)[offset:limit])

    def solve_ticket(self, ticket_id):
        """Marks a ticket as solved."""
        Ticket.objects.update(solved=True).filter(ticket_id=ticket_id)

    def delete_ticket(self, ticket_id):
        """Deletes a ticket from the database."""
        Occurrence.objects.get(ticket_id=ticket_id).delete()
        Ticket.objects.get(ticket_id=ticket_id).delete()

    def get_ticket(self, ticket_id):
        """Return a single ticket with all occurrences."""
        try:
            return Ticket.objects.get(ticket_id=ticket_id)
        except Ticket.DoesNotExist:
            return Ticket()

    def get_occurrences(self, ticket, order_by='-time', limit=50, offset=0):
        """Selects occurrences from the database for a ticket."""
        return list(
            Occurrence.objects \
                .filter(ticket_id=ticket) \
                .order_by(order_by)[offset:limit])
