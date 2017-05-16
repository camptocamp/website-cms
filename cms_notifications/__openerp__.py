# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'CMS notifications',
    'summary': """Basic notifications management for your CMS system""",
    'version': '9.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Camptocamp,Odoo Community Association (OCA)',
    'depends': [
        'cms_form',
        'mail_digest',
    ],
    'data': [
        'views/mail_message_subtype_views.xml',
        'templates/assets.xml',
        'templates/help_msg.xml',
        'templates/widget.xml',
        'templates/notification_listing.xml',
    ],
}
