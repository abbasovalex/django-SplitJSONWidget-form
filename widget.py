# -*- coding: utf8 -*-
from django import forms
from django.forms import Widget
from django import utils
#import ast
#import itertools
#from django.utils.translation import ugettext_lazy as _
import copy
try:
    import simplejson as json
except ImportError:
    import json


class SplitJSONWidget(forms.Widget):

    def __init__(self, attrs=None, newline='<br/>\n', sep='__', debug=False):
        self.newline = newline
        self.separator = sep
        self.debug = debug
        Widget.__init__(self, attrs)

    def _as_text_field(self, name, key, value, is_sub=False):
        attrs = self.build_attrs(self.attrs, type='text',
                                 name="%s%s%s" % (name, self.separator, key))
        attrs['value'] = utils.encoding.force_unicode(value)
        attrs['id'] = attrs.get('name', None)
        return u""" <label for="%s">%s:</label>
        <input%s />""" % (attrs['id'], key, forms.util.flatatt(attrs))

    def _to_build(self, name, json_obj):
        inputs = []
        if type(json_obj) is list:
            title = name.rpartition(self.separator)[2]
            _l = ['%s:%s' % (title, self.newline)]
            for key, value in enumerate(json_obj):
                _l.append(self._to_build("%s%s%s" % (name,
                                         self.separator, key), value))
            inputs.extend([_l])
        elif type(json_obj) is dict:
            title = name.rpartition(self.separator)[2]
            _l = ['%s:%s' % (title, self.newline)]
            for key, value in json_obj.items():
                _l.append(self._to_build("%s%s%s" % (name,
                                                     self.separator, key),
                                         value))
            inputs.extend([_l])
        elif type(json_obj) in (str, unicode, int):
            name, _, key = name.rpartition(self.separator)
            inputs.append(self._as_text_field(name, key, json_obj))
        elif json_obj is None:
            name, _, key = name.rpartition(self.separator)
            inputs.append(self._as_text_field(name, key, ''))
        return inputs

    def _prepare_as_ul(self, l):
        if l:
            result = u'<ul>'
            for el in l:
                if type(el) is list:
                    result += '%s' % self._prepare_as_ul(el)
                else:
                    result += '<li>%s</li>' % el
            result += '</ul>'
            return result
        return ''

    def _to_pack_up(self, root_node, raw_data):

        old_obj = raw_data
        new_obj = {root_node: None}

        def _key_to_list(k):
            obj = {}
            result = []
            for key, v in old_obj.items():
                if key.startswith(k):
                    apx, s, nk = key.rpartition(self.separator)
                    # to transform value from list to string
                    v = v[0] if type(v) is list and len(v) is 1 else v
                    try:
                        int(nk)
                        obj = v
                    except ValueError:
                        obj[nk] = v
                    del old_obj[key]
            if obj:
                result.append(obj)
                return result
            return result

        def _key_to_dict(k, obj):
            if k.find(self.separator) is not -1:
                apx, s, nk = k.rpartition(self.separator)
                try:
                    int(nk)
                    return _key_to_dict(apx, _key_to_list(k))
                except ValueError:
                    obj = {nk: obj}
                    return _key_to_dict(apx, obj)
            return obj

        for k, v in old_obj.items():
            # to transform value from list to string
            v = v[0] if type(v) is list and len(v) is 1 else v

            if k.find(self.separator) is not -1:
                apx, s, nk = k.rpartition(self.separator)
                try:
                    int(nk)
                    d = _key_to_dict(apx, _key_to_list(k))
                except ValueError:
                    d = _key_to_dict(k, v)

                #merge
                keys = d.keys()
                for k in keys:
                    if k in new_obj:
                        if type(new_obj[k]) is list and len(d[k]):
                            new_obj[k].extend(d[k])
                        elif type(new_obj[k]) is dict and len(d[k]):
                            new_obj[k].update(d[k])
                    else:
                        new_obj.update(d)

        return new_obj

    def value_from_datadict(self, data, files, name):
        data_copy = copy.deepcopy(data)
        result = self._to_pack_up(name, data_copy)
        return json.dumps(result)

    def render(self, name, value, attrs=None):
        try:
            value = json.loads(value)
        except TypeError:
            pass
        inputs = self._to_build(name, value or {})
        result = self._prepare_as_ul(inputs)
        if self.debug:
            # render json as well
            source_data = u'<hr/>Source data: <br/>%s<hr/>' % str(value)
            result = '%s%s' % (result, source_data)
            print result
        return utils.safestring.mark_safe(result)
