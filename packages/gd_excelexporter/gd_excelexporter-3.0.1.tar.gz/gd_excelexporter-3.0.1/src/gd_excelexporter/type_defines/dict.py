"""
author:        kaluluosi111 <kaluluosi@gmail.com>
date:          2024-04-16 11:30:30
Copyright © Kaluluosi All rights reserved
"""

from gd_excelexporter.core.type_define import TypeDefine


class Dict(TypeDefine):
    def _convert(self, raw_value: str, id=None):
        _value = eval(f'{{{raw_value.replace("|",",")}}}') if raw_value else {}
        return _value
