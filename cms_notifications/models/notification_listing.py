# -*- coding: utf-8 -*-
# Copyright 2017 Simone Orsi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, _


class CMSNotificationListing(models.AbstractModel):
    """Hold users notifications settings."""
    _name = 'cms.notification.listing'
    _inherit = 'cms.form.search'
    _description = 'CMS notifications'

    _form_model = 'mail.message'
    _form_model_fields = (
        'subtype_id',
    )
    form_search_results_template = 'cms_notifications.listing'
    # form_wrapper_template = 'cms_notifications.notifications_wrapper'
    # form_template = 'cms_notifications.notifications_search_form'

    @property
    def form_title(self):
        return _('My notifications')

    @property
    def form_description(self):
        return ''

    @property
    def _super(self):
        return super(CMSNotificationListing, self)

    def form_search_domain(self, search_values):
        domain = self._super.form_search_domain(search_values)
        default_domain = [
            ('partner_ids', 'in', [self.env.user.partner_id.id, ]),
            ('subtype_id.cms_type', '=', True),
        ]
        domain.extend(default_domain)
        return domain
