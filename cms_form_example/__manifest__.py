# Copyright 2017 Simone Orsi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "CMS Form example",
    "summary": """
        Basic content type form example""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Simone Orsi,Odoo Community Association (OCA)",
    "maintainers": ["simahawk"],
    "website": "https://github.com/OCA/website-cms",
    "depends": [
        "website_partner",
        "cms_form",
    ],
    "assets": {
        "web.assets_frontend": [
            "cms_form_example/static/src/js/cms_form_example.tour.js",
        ],
    },
    "installable": True,
}
