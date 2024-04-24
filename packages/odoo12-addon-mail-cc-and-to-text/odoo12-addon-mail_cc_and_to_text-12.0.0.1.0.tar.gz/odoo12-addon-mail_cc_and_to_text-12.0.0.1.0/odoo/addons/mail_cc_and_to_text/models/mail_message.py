# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class Message(models.Model):
    """Messages model: system notification (replacing res.log notifications),
    comments (OpenChatter discussion) and incoming emails."""

    _inherit = "mail.message"

    origin_email_to = fields.Char("To", help="Message recipients (emails)")
    origin_email_cc = fields.Char("Cc", help="Carbon copy message recipients")
