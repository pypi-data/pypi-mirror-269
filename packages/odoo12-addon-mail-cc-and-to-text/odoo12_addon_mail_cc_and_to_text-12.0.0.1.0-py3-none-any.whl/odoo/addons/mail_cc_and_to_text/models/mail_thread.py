# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models
import re
import email

try:
    from xmlrpc import client as xmlrpclib
except ImportError:
    import xmlrpclib
from odoo.tools import pycompat


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def clean_email_cc(self, email_cc):
        # The pattern looks for anything XXXX@XXXX.XXX
        patron = r"[\w\.-]+@[\w\.-]+"

        # Find all matches using findall instead of a loop
        matches = re.findall(patron, email_cc)

        # Join all matches with comma separator
        cleaned_cc = ",".join(matches)

        return cleaned_cc

    @api.model
    def message_process(
        self,
        model,
        message,
        custom_values=None,
        save_original=False,
        strip_attachments=False,
        thread_id=None,
    ):
        thread_id = super(MailThread, self).message_process(
            model, message, custom_values, save_original, strip_attachments, thread_id
        )

        # extract message bytes - we are forced to pass the message as binary because
        # we don't know its encoding until we parse its headers and hence can't
        # convert it to utf-8 for transport between the mailgate script and here.
        message = message
        if isinstance(message, xmlrpclib.Binary):
            message = bytes(message.data)
        # message_from_string parses from a *native string*, except apparently
        # sometimes message is ISO-8859-1 binary data or some shit and the
        # straightforward version (pycompat.to_native) won't work right ->
        # always encode message to bytes then use the relevant method
        # depending on ~python version
        if isinstance(message, pycompat.text_type):
            message = message.encode("utf-8")
        extract = getattr(email, "message_from_bytes", email.message_from_string)
        msg_txt = extract(message)

        # parse the message, verify we are not in a loop by checking message_id
        # is not duplicated
        msg = self.message_parse(msg_txt, save_original=save_original)

        mail_message = self.env["mail.message"].search(
            [("message_id", "=", msg.get("message_id"))]
        )
        if mail_message:
            mail_message.write(
                {
                    "origin_email_cc": self.clean_email_cc(msg.get("cc", "")),
                    "origin_email_to": self.clean_email_cc(msg.get("to", "")),
                }
            )

        mail_mail = self.env["mail.mail"].search(
            [("message_id", "=", msg.get("message_id"))]
        )
        if mail_mail:
            mail_mail.write(
                {
                    "email_cc": self.clean_email_cc(msg.get("cc", "")),
                    "email_to": self.clean_email_cc(msg.get("to", "")),
                }
            )
        return thread_id
