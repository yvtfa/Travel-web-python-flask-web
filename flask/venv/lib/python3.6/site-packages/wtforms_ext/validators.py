# -*- coding: utf-8 -*-

from wtforms.validators import ValidationError, StopValidation


class OrRequiredWith(object):
    """用于验证多个表单字段必填一个"""
    def __init__(self, fieldnames, message=None):
        self.message = message
        self.fieldnames = fieldnames
        for fieldname in fieldnames:
            setattr(self, fieldname, fieldname)

    def __call__(self, form, field):
        fields = list()
        if not field.data:
            for fieldname in self.fieldnames:
                try:
                    fields.append(form[getattr(self, fieldname)])
                    other = form[getattr(self, fieldname)]
                except KeyError:
                    raise ValidationError(field.gettext("Invalid field name '%s'.") % getattr(self, fieldname))

                if other.data:
                    field.errors[:] = []
                    raise StopValidation()
            else:
                self.fieldnames.append(field.name)

                d = {
                    'fieldnames': ', '.join(list(set(self.fieldnames)))
                }
                message = self.message
                if message is None:
                    message = field.gettext('At least one field is required in %(fieldnames)s.')
                raise ValidationError(message % d)


class AndRequiredWith(object):
    """用于验证多个表单字段均必填"""
    def __init__(self, fieldnames, message=None):
        self.message = message
        self.fieldnames = fieldnames
        for fieldname in fieldnames:
            setattr(self, fieldname, fieldname)

    def __call__(self, form, field):
        fields = list()
        if not field.data:
            for fieldname in self.fieldnames:
                try:
                    fields.append(form[getattr(self, fieldname)])
                    other = form[getattr(self, fieldname)]
                    if not other.data:
                        break
                except KeyError:
                    raise ValidationError(field.gettext("Invalid field name '%s'.") % getattr(self, fieldname))
            else:
                self.fieldnames.append(field.name)

                d = {
                    'fieldnames': ', '.join(list(set(self.fieldnames)))
                }
                message = self.message
                if message is None:
                    message = field.gettext('All fields are required in %(fieldnames)s.')
                raise ValidationError(message % d)


def validate_select_relation(original_field_name, keys=[u'其他', u'其它']):
    """
    用以验证 SelectField 选择制定选项时关联的扩展字段是否填写
    :param original_field_name 对应的 SelectField 的 name
    :param keys 匹配的选项列表
    """
    def _validate_other(form, field):
        original_field = getattr(form, original_field_name)
        key_list = [keys] if not isinstance(keys, list) else keys
        if dict(getattr(original_field, 'choices')).get(getattr(original_field, 'data')) in key_list:
            if not field.data:
                message = u'请填写{0}！'.format(field.label.text)
                raise ValidationError(message)

    return _validate_other
