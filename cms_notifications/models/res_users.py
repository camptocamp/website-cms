# -*- coding: utf-8 -*-
# © 2017  Simone Orsi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    has_unread_notif = fields.Boolean(
        string='Has unread notif',
        compute='_compute_has_unread_notif',
        readonly=True,
    )

    @api.multi
    @api.depends()
    def _compute_has_unread_notif(self):
        msg_model = self.env['mail.message']
        for item in self:
            if not item.partner_id:
                continue
            domain = [
                ('partner_ids', 'in', item.partner_id.id),
                ('needaction_partner_ids', 'in', item.partner_id.id),
                ('subtype_id.cms_type', '=', True),
            ]
            item.has_unread_notif = bool(msg_model.search_count(domain))
