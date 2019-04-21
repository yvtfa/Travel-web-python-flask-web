# -*- coding: utf-8 -*-


def get_data_field_names(form, model):
    """获取对应 Form 的数据列名称"""
    return list(set([field.name for field in form()]).intersection([col for col in model().__table__.columns.keys()]))
