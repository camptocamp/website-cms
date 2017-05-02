# -*- coding: utf-8 -*-

from openerp import http
from openerp.addons.cms_form.controllers.main import FormControllerMixin


class PanelFormController(http.Controller, FormControllerMixin):
    """Notification panel form controller."""

    @http.route([
        '/my/settings/notification',
    ], type='http', auth='user', website=True)
    def cms_form(self, **kw):
        model = 'res.partner'
        # get current user partner
        model_id = http.request.env.user.partner_id.id
        return self.make_response(
            model, model_id=model_id, **kw)

    def form_model_key(self, model):
        return 'cms.notification.panel.form'
