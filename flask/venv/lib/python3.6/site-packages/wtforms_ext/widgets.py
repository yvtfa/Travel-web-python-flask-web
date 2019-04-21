# -*- coding: utf-8 -*-

from wtforms.widgets import HTMLString, html_params, TextArea, Select
from wtforms.compat import text_type
try:
    from html import escape
except ImportError:
    from cgi import escape


# https://gist.github.com/playpauseandstop/1590178
class ExtendedSelectWidget(Select):
    """Add support of choices with ``optgroup`` to the ``Select`` widget."""
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if self.multiple:
            kwargs['multiple'] = True
        html = ['<select %s>' % html_params(name=field.name, **kwargs)]
        for item1, item2 in field.choices:
            if isinstance(item2, (list, tuple)):
                group_label = item1
                group_items = item2
                html.append('<optgroup %s>' % html_params(label=group_label))
                for inner_val, inner_label in group_items:
                    html.append(self.render_option(inner_val, inner_label, inner_val == field.data))
                html.append('</optgroup>')
            else:
                val = item1
                label = item2
                html.append(self.render_option(val, label, val == field.data))
        html.append('</select>')
        return HTMLString(''.join(html))


class FilterSelectWidget(Select):
    """Add support of choices with ``display`` to the ``Select`` widget."""
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if self.multiple:
            kwargs['multiple'] = True
        html = ['<select %s>' % html_params(name=field.name, **kwargs)]
        for val, label, display in field.choices:
            html.append(self.render_option(val, label, val == field.data, display))
        html.append('</select>')
        return HTMLString(''.join(html))

    @classmethod
    def render_option(cls, value, label, selected, display):
        if value is True:
            # Handle the special case of a 'True' value.
            value = text_type(value)

        options = dict(value=value)
        if selected:
            options['selected'] = True
        if not display:
            options['style'] = 'display: none;'
        return HTMLString('<option %s>%s</option>' % (html_params(**options), escape(text_type(label), quote=False)))


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        # Add WYSIWYG class to existing classes
        existing_classes = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'%s %s' % (existing_classes, "ckeditor")
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)
