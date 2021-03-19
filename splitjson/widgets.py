# -*- coding: utf-8 -*-
import copy
try:
    import simplejson as json
except ImportError:
    import json

from django.forms import Widget
from django.forms.utils import flatatt
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe


class SplitJSONWidget(Widget):
    """
    Widget to render a single JSONField as a series of text inputs.
    """

    def __init__(self, attrs=None, newline='<br/>\n', sep='__', debug=False):
        self.newline = newline
        self.separator = sep
        self.debug = debug
        Widget.__init__(self, attrs)

    def _as_text_field(self, name, key, value):
        attrs = self.build_attrs(
            self.attrs,
            {
                'type': 'text',
                'name': f'{name}{self.separator}{key}',
            },
        )
        attrs['value'] = force_str(value)
        attrs['id'] = attrs.get('name', None)
        return (
            f"""<label for="{attrs['id']}">{key}:</label>"""
            f'<input{flatatt(attrs)} />'
        )

    def _to_build(self, name, json_obj):
        inputs = []
        if isinstance(json_obj, list):
            title = name.rpartition(self.separator)[2]
            _l = [f'{title}:{self.newline}']
            for key, value in enumerate(json_obj):
                _l.append(
                    self._to_build(
                        f'{name}{self.separator}{key}',
                        value,
                    )
                )
            inputs.extend([_l])
        elif isinstance(json_obj, dict):
            title = name.rpartition(self.separator)[2]
            _l = [f'{title}:{self.newline}']
            for key, value in json_obj.items():
                _l.append(
                    self._to_build(
                        f'{name}{self.separator}{key}',
                        value,
                    )
                )
            inputs.extend([_l])
        elif isinstance(json_obj, (str, int, float)):
            name, _, key = name.rpartition(self.separator)
            inputs.append(self._as_text_field(name, key, json_obj))
        elif json_obj is None:
            name, _, key = name.rpartition(self.separator)
            inputs.append(self._as_text_field(name, key, ''))
        return inputs

    def _prepare_as_ul(self, l):
        if l:
            result = ''
            for el in l:
                if isinstance(el, list) and len(l) == 1:
                    result += str(self._prepare_as_ul(el))
                elif isinstance(el, list):
                    result += f'<ul>{self._prepare_as_ul(el)}</ul>'
                else:
                    result += f'<li>{el}</li>'
            return result
        return ''

    def _to_pack_up(self, root_node, raw_data):

        copy_raw_data = copy.deepcopy(raw_data)
        result = []

        def _to_parse_key(k, v):
            if k.find(self.separator) != -1:
                apx, _, nk = k.rpartition(self.separator)
                try:
                    # parse list
                    int(nk)
                    l = []
                    obj = {}
                    if apx != root_node:
                        for key, val in copy_raw_data.items():
                            head, _, t = key.rpartition(self.separator)
                            _, _, index = head.rpartition(self.separator)
                            if key is k:
                                del copy_raw_data[key]
                            elif key.startswith(apx):
                                try:
                                    int(t)
                                    l.append(val)
                                except ValueError:
                                    if index in obj:
                                        obj[index].update({t: val})
                                    else:
                                        obj[index] = {t: val}
                                del copy_raw_data[key]
                        if obj:
                            for i in obj:
                                l.append(obj[i])
                    l.append(v)
                    return _to_parse_key(apx, l)
                except ValueError:
                    # parse dict
                    d = {}
                    if apx != root_node:
                        for key, val in copy_raw_data.items():
                            _, _, t = key.rpartition(self.separator)
                            try:
                                int(t)
                                continue
                            except ValueError:
                                pass
                            if key is k:
                                del copy_raw_data[key]
                            elif key.startswith(apx):
                                d.update({t: val})
                                del copy_raw_data[key]
                    v = {nk: v}
                    if d:
                        v.update(d)
                    return _to_parse_key(apx, v)
            else:
                return v

        for k, v in raw_data.items():
            if k in copy_raw_data:
                # to transform value from list to string
                v = v[0] if isinstance(v, list) and len(v) is 1 else v
                if k.find(self.separator) != -1:
                    d = _to_parse_key(k, v)
                    # set type result
                    if not len(result):
                        result = type(d)()
                    try:
                        result.extend(d)
                    except Exception:
                        result.update(d)
        return result

    def value_from_datadict(self, data, files, name):
        data_copy = copy.deepcopy(data)
        result = self._to_pack_up(name, data_copy)
        return json.dumps(result)

    def render(self, name, value, attrs=None, renderer=None):
        try:
            value = json.loads(value)
        except (TypeError, KeyError):
            pass
        inputs = self._to_build(name, value or {})
        result = self._prepare_as_ul(inputs)
        if self.debug:
            # render json as well
            source_data = f'<hr/>Source data: <br/>{value}<hr/>'
            result = f'{result}{source_data}'
        return mark_safe(result)
