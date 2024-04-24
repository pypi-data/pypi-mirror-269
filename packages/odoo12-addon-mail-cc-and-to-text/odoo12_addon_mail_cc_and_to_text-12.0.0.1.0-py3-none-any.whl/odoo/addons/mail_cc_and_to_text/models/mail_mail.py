# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, api
from odoo.tools import formataddr


class MailMail(models.Model):
    """Messages model: system notification (replacing res.log notifications),
    comments (OpenChatter discussion) and incoming emails."""

    _inherit = "mail.mail"

    @api.model
    def create(self, values):
        mail = super(MailMail, self).create(values)
        if mail.recipient_ids:
            res_partner = (
                self.env["res.partner"]
                .sudo()
                .search([("id", "in", mail.recipient_ids.ids)])
            )
            if mail.email_to:
                mail.write(
                    {
                        "origin_email_to": mail.email_to,
                    }
                )
            else:
                mail.write(
                    {
                        "origin_email_to": ",".join(
                            formataddr((partner.name, partner.email))
                            for partner in res_partner
                            if partner.email
                        ),
                    }
                )
        return mail
