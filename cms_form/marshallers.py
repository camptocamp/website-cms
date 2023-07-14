# Copyright 2018 Simone Orsi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import html
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


def marshal_request_values(values):
    """Transform given request values using marshallers.

    Available marshallers:

    * `:int` transform to integer
    * `:float` transform to float
    * `:list` transform to list of values
    * `:dict` transform to dictionary of values
    """
    # TODO: add docs
    # TODO: support combinations like `:list:int` or `:dict:int`
    return Marshaller(values).marshall()


@dataclass
class Todo:
    okey: str
    oval: Any
    handlers: list[Callable]


class Marshaller:
    def __init__(self, req_values):
        self.req_values = req_values
        self.todos = []
        self.skip_keys = {"csrf_token"}
        self._collect_todo()

    def _add_todo(self, orig_key, orig_value, *handlers):
        self.todos.append(Todo(okey=orig_key, oval=orig_value, handlers=handlers))

    def _collect_todo(self):
        for k, v in self.req_values.items():
            if k in self.skip_keys:
                continue
            if k.endswith(":esc"):
                self._add_todo(k, v, self.marshal_esc)
                continue
            if k.endswith(":list"):
                self._add_todo(k, v, self.marshal_list)
                continue
            if k.endswith(":dict"):
                self._add_todo(k, v, self.marshal_dict)
                continue
            if k.endswith(":int"):
                self._add_todo(k, v, self.marshal_int)
                continue
            if k.endswith(":float"):
                self._add_todo(k, v, self.marshal_float)
                continue
            # plain
            self._add_todo(k, v, self.marshal_plain)

    def marshall(self):
        res = {}
        for todo in self.todos:
            k, v = todo.okey, todo.oval
            for handler in todo.handlers:
                k, v = handler(k, v)
            res[k] = v
        return res

    def marshal_plain(self, orig_key, orig_value):
        """No transform."""
        return orig_key, orig_value

    def marshal_esc(self, orig_key, orig_value):
        """Transform `foo:esc` inputs to escaped value."""
        k = orig_key[: -len(":esc")]
        v = html.escape(orig_value)
        return k, v

    def marshal_list(self, orig_key, orig_value):
        """Transform `foo:list` inputs to list of values."""
        k = orig_key[: -len(":list")]
        v = self.req_values.getlist(orig_key)
        return k, v

    def marshal_int(self, orig_key, orig_value):
        """Transform `foo:int` inputs to integer values."""
        k = orig_key[: -len(":int")]
        v = int(orig_value) if orig_value and orig_value.isdigit() else orig_value
        return k, v

    def marshal_float(self, orig_key, orig_value):
        """Transform `foo:float` inputs to float values."""
        k = orig_key[: -len(":float")]
        try:
            v = float(orig_value.replace(",", "."))
        except (ValueError, TypeError):
            v = orig_value
        return k, v

    def marshal_dict(self, orig_key, orig_value):
        """Transform `foo:dict` inputs to dictionary values.

        `orig_key` must be formatted like:

            `$fname.$dict_key:dict`

        Every request key matching `$fname` prefix
        will be merged into a dict whereas keys will match all `$dict_key`.

        Example:

            values = [
                ('foo.a:dict', '1'),
                ('foo.b:dict', '2'),
                ('foo.c:dict', '3'),
            ]

            will be translated to:

            values['foo'] = {
                'a': '1',
                'b': '2',
                'c': '3',
            }

        """
        res = {}
        key = orig_key.split(".")[0]
        for _k, _v in self.req_values.items():
            # get all the keys matching fname
            if not _k.startswith(key):
                continue
            # TODO: `__` will be to support extra marshallers, like:
            # foo.1:dict:int -> get a dictionary w/ integer values
            full_key, _, __ = _k.partition(":dict")
            res[full_key.split(".")[-1]] = _v
        return key, res
