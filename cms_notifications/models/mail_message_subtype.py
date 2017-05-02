# -*- coding: utf-8 -*-

from openerp import fields, models


class MailMessageSubtype(models.Model):
    _inherit = 'mail.message.subtype'

    cms_type = fields.Boolean(
        'Visible in CMS control panel',
        help=("If active, this message subtype will be visible "
              "in users' notifications control panel.")
    )
