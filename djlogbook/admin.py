from django.contrib import admin
from django.template.defaultfilters import escape

from .models import Ticket, Occurrence


class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'ticket_id',
        'level',
        'channel',
        'module',
        'last_occurrence_time',
        'occurrence_count',
        'solved')
    list_filter = (
        'level', 'channel', 'module', 'last_occurrence_time', 'solved')

admin.site.register(Ticket, TicketAdmin)


class OccurrenceAdmin(admin.ModelAdmin):
    readonly_fields = ('data', 'message', 'html_formatted_exception')
    list_display = (
        'occurrence_id',
        'ticket',
        'short_message',
        'time',
        'app_id')
    list_filter = ('ticket', 'time', 'app_id')
    raw_id_fields = ('ticket',)

    # TODO: move to template
    def html_formatted_exception(self, obj):
        return '<textarea rows="10" cols="40" name="data" class="vLargeTextField">%s</textarea>' % escape(obj.formatted_exception)

    html_formatted_exception.allow_tags = True

admin.site.register(Occurrence, OccurrenceAdmin)
