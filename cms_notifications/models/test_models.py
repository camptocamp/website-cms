# -*- coding: utf-8 -*-
# Copyright 2017 Simone Orsi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, tools

testing = tools.config.get('test_enable')


if testing:
    class CMSNotificationPanel(models.AbstractModel):

        _inherit = 'cms.notification.panel.form'

        enable_1 = fields.Boolean(string='Enable 1')
        enable_2 = fields.Boolean(string='Enable 2')
        enable_3 = fields.Boolean(string='Enable 3')

        @property
        def _form_subtype_fields(self):
            res = super(CMSNotificationPanel, self)._form_subtype_fields
            res.update({
                'enable_1': 'cms_notifications.test_subtype1',
                'enable_2': 'cms_notifications.test_subtype2',
                'enable_3': 'cms_notifications.test_subtype3',
            })
            return res
