# Copyright 2018 Simone Orsi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from ..common import get_form
from .common import TestWidgetCase


def fake_field(name, **kw):
    info = {
        'type': 'char',
        'required': False,
        'string': name.capitalize(),
        'readonly': False,
        'help': 'Help for %s' % name,
    }
    info.update(kw)
    return name, info


class TestWidgetBase(TestWidgetCase):

    def test_widget_init(self):
        form = get_form(self.env, 'cms.form.res.partner')
        field = form.form_fields()['custom']
        widget = self.get_widget('custom', field, form=form)
        self.assertEqual(widget.w_form, form)
        self.assertEqual(widget.w_form_model, form.form_model)
        self.assertEqual(widget.w_record, form.main_object)
        self.assertEqual(widget.w_form_values, form.form_render_values)
        self.assertEqual(widget.w_fname, 'custom')
        self.assertDictEqual(widget.w_field, field)
        self.assertEqual(widget.w_field_value, None)
        self.assertEqual(widget.w_data, {})
        self.assertEqual(widget.w_subfields, {})
    
    def test_w_load(self):
        name, field = fake_field('foo')
        widget = self.get_widget(
            name, field, widget_model='cms.form.widget.char')
        # no value from default, nor from request, nor from record
        self.assertEqual(widget.w_load(), None)
        # get value from default. Default values from ORM
        # are stored into internal key `_default` by `cms.form.mixin`
        field['_default'] = 'oh yeah'
        widget = self.get_widget(
            name, field, widget_model='cms.form.widget.char')
        self.assertEqual(widget.w_load(), 'oh yeah')
        # get value from request and it has precedence over default
        self.assertEqual(widget.w_load(foo='daje'), 'daje')
        # get value from record (faked here)
        widget.w_record = {'foo': 'value coming from record'}
        self.assertEqual(widget.w_load(), 'value coming from record')
        # still, value from request takes precedence
        self.assertEqual(
            widget.w_load(foo='I am more important'), 'I am more important')

    def test_w_extract(self):
        name, field = fake_field('foo')
        widget = self.get_widget(
            name, field, widget_model='cms.form.widget.char')
        # no val in request
        self.assertEqual(widget.w_extract(), None)
        self.assertEqual(widget.w_extract(foo='yo!'), 'yo!')

    def test_w_ids_from_input(self):
        name, field = fake_field('foo')
        widget = self.get_widget(
            name, field, widget_model='cms.form.widget.char')
        self.assertEqual(widget.w_ids_from_input(''), [])
        self.assertEqual(widget.w_ids_from_input(
            '1,2,3,#4, 70, 1oo', ), [1, 2, 3, 70])