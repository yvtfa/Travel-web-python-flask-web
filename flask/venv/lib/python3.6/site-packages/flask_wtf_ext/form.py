# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms.compat import iteritems
from wtforms_ext import ExtendedFormField, ExtendedFieldList


class ExtendedFlaskForm(FlaskForm):
    def populate_obj(self, obj, ignore_fields=None):
        """
        Populates the attributes of the passed `obj` with data from the form's
        fields.
        :note: This is a destructive operation; Any attribute with the same name
               as a field will be overridden. Use with caution.
        :param ignore_fields:
            Fields that should not be populated.
        """
        if ignore_fields is None:
            ignore_fields = []

        for name, field in iteritems(self._fields):
            if name in ignore_fields:
                continue

            if isinstance(field, (ExtendedFormField, ExtendedFieldList)):
                field.populate_obj(obj, name, ignore_fields=ignore_fields)
            else:
                field.populate_obj(obj, name)
