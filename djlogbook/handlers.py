import logbook

from django.core import mail


MAIL_FORMAT_STRING = u'''\
URI: {record.extra[absolute_uri]}
IP: {record.extra[ip]}
Message type: {record.level_name}
Location: {record.filename}:{record.lineno}
Module: {record.module}
Function: {record.func_name}
Time: {record.time:%Y-%m-%d %H:%M:%S}

Message:

{record.message}
'''


class DjangoMailHandler(logbook.MailHandler):
    default_format_string = MAIL_FORMAT_STRING

    def deliver(self, msg, recipients):
        """Delivers the given message to a list of recpients."""

        mail.send_mail(
            self.subject,
            msg.as_string(),
            self.from_addr,
            recipients,
            fail_silently=True)
