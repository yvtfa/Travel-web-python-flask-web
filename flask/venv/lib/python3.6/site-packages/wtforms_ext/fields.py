# -*- coding: utf-8 -*-

import itertools
from wtforms.fields import SelectField, FormField, TextAreaField, SelectMultipleField, FieldList
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.compat import izip
from wtforms.utils import unset_value
from .widgets import ExtendedSelectWidget, FilterSelectWidget, CKTextAreaWidget


# https://gist.github.com/playpauseandstop/1590178
class ExtendedSelectField(SelectField):
    """
    Add support of ``optgroup`` grouping to default WTForms' ``SelectField`` class.
    Here is an example of how the data is laid out.
        (
            ('Fruits', (
                ('apple', 'Apple'),
                ('peach', 'Peach'),
                ('pear', 'Pear')
            )),
            ('Vegetables', (
                ('cucumber', 'Cucumber'),
                ('potato', 'Potato'),
                ('tomato', 'Tomato'),
            )),
            ('other','None Of The Above')
        )
    It's a little strange that the tuples are (value, label) except for groups which are (Group Label, list of tuples)
    but this is actually how Django does it too https://docs.djangoproject.com/en/dev/ref/models/fields/#choices
    """
    widget = ExtendedSelectWidget()

    def pre_validate(self, form):
        """Don't forget to validate also values from embedded lists."""
        for item1, item2 in self.choices:
            if isinstance(item2, (list, tuple)):
                group_label = item1
                group_items = item2
                for val, label in group_items:
                    if val == self.data:
                        return
            else:
                val = item1
                label = item2
                if val == self.data:
                    return
        raise ValueError(self.gettext('Not a valid choice!'))


class FilterSelectField(SelectField):
    """
    Added support for displaying option or not.
    Here is an example of how the data is laid out.
        [(0, 'zengqiu', True), (1, 'zhouying', False)]
    """
    widget = FilterSelectWidget()

    def pre_validate(self, form):
        for val, label, display in self.choices:
            if val == self.data:
                return
        raise ValueError(self.gettext('Not a valid choice!'))


class ExtendedFormField(FormField):
    """用于配合 ExtendedForm 使用（添加 populate 时忽略的字段）"""
    def process(self, formdata, data=unset_value):
        if data is unset_value or not data:
            try:
                data = self.default()
            except TypeError:
                data = self.default
            self._obj = data

        self.object_data = data

        prefix = self.name + self.separator
        if isinstance(data, dict):
            self.form = self.form_class(formdata=formdata, prefix=prefix, **data)
        else:
            self.form = self.form_class(formdata=formdata, obj=data, prefix=prefix)

    def populate_obj(self, obj, name, ignore_fields):
        candidate = getattr(obj, name, None)
        if candidate is None:
            if self._obj is None:
                raise TypeError('populate_obj: cannot find a value to populate from the provided obj or input data/defaults')
            candidate = self._obj
            setattr(obj, name, candidate)

        self.form.populate_obj(candidate, ignore_fields)


class ExtendedFieldList(FieldList):
    """用于配合 ExtendedForm 使用（添加 populate 时忽略的字段）"""
    def populate_obj(self, obj, name, ignore_fields):
        values = getattr(obj, name, None)
        try:
            ivalues = iter(values)
        except TypeError:
            ivalues = iter([])

        candidates = itertools.chain(ivalues, itertools.repeat(None))
        _fake = type(str('_fake'), (object,), {})
        output = []
        for field, data in izip(self.entries, candidates):
            fake_obj = _fake()
            fake_obj.data = data
            field.populate_obj(fake_obj, 'data', ignore_fields)
            output.append(fake_obj.data)

        setattr(obj, name, output)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class NonValidatingSelectField(SelectField):
    """无验证选择（主要用于 Ajax 获取选项）"""
    def pre_validate(self, form):
        pass


class NonValidatingSelectMultipleField(SelectMultipleField):
    def pre_validate(self, form):
        pass
