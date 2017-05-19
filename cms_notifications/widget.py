# -*- coding: utf-8 -*-
# Copyright 2017 Simone Orsi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.addons.cms_form.widgets import RadioSelectionWidget


class NotificationSelectionWidget(RadioSelectionWidget):
    key = 'cms_notifications.field_widget_notification_selection'
    help_tmpl_prefix = 'cms_notifications.notify_email_help_'

    @property
    def option_items(self):
        """Change options order and inject help text."""
        items = []
        sel = dict(self.field['selection'])
        for item in ('always', 'digest', 'none', ):
            template = self.env.ref(
                self.help_tmpl_prefix + item, raise_if_not_found=0)
            _help = None
            if template:
                _help = template.render({'sel': sel, 'field': self.field})
            items.append({
                'value': item,
                'label': sel[item],
                'help': _help
            })
        return items
