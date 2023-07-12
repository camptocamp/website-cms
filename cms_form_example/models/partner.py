# Copyright 2017 Simone Orsi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools

from odoo.addons.cms_form.models.fields import Serialized

testing = tools.config.get("test_enable")


if not testing:
    # prevent these forms to be registered when running tests

    class ExamplePartnerForm(models.AbstractModel):
        """A test model form."""

        _name = "cms.form.res.partner"
        _inherit = "cms.form"
        _description = __doc__

        form_model_name = fields.Char(default="res.partner")
        form_model_fields = Serialized(default=("name", "country_id", "category_id"))
        form_required_fields = Serialized(default=("name",))
        form_fields_order = Serialized(default=("name", "country_id", "category_id"))

        custom = fields.Char()

        def _form_load_custom(self, form, main_object, fname, value, **req_values):
            """Load a custom default for the field 'custom'."""
            return req_values.get("custom", "oh yeah!")

    class PartnerSearchForm(models.AbstractModel):
        """Partner model search form."""

        _name = "cms.form.search.res.partner"
        _inherit = "cms.form.search"
        _description = __doc__
        form_model_name = fields.Char(default="res.partner")
        form_model_fields = Serialized(default=("name", "country_id"))

    class PartnerSearchFormAjax(models.AbstractModel):
        """Partner model search form with ajax."""

        _inherit = "cms.form.search.res.partner"
        _name = "cms.form.search.res.partner.ajax"
        _description = __doc__
        form_ajax = fields.Boolean(default=True)
        form_ajax_onchange = fields.Boolean(default=True)

    class ExamplePartnerFormWithFieldsets(models.AbstractModel):
        _name = "cms.form.res.partner.fset"
        _inherit = "cms.form.res.partner"
        _description = __doc__

        form_fieldsets = Serialized(
            default=[
                {
                    "id": "main",
                    "title": "Main",
                    "fields": [
                        "name",
                        "category_id",
                    ],
                },
                {
                    "id": "secondary",
                    "title": "Secondary",
                    "fields": [
                        "country_id",
                    ],
                },
            ]
        )

    class ExamplePartnerFormWithTabbedFieldsets(models.AbstractModel):
        _name = "cms.form.res.partner.fset.tabbed"
        _inherit = "cms.form.res.partner.fset"

        form_fieldsets_display = fields.Selection(default="tabs")
