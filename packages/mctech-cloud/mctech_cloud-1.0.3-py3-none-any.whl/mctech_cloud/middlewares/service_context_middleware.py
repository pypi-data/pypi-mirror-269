import re
import math

from typing import Dict, Callable
from starlette.datastructures import Headers
from starlette.types import ASGIApp, Receive, Scope, Send
from mctech_core.context import get_async_context, WebContext, \
    header_filter as filter

pattern = re.compile('-([a-z])', re.IGNORECASE)


def try_convert_number(val: str):
    ret = int(val)
    return val if math.isnan(ret)else ret


_converters: Dict[str, Callable[[str], any]] = {
    'x-tenant-id': try_convert_number,
    'x-user-id': try_convert_number,
    'x-id': try_convert_number,
    'x-org-id': try_convert_number
}


class ServiceContextMiddleware:
    def __init__(self,
                 app: ASGIApp,
                 converters: Dict[str, Callable[[str], any]]):
        self._app = app
        self._converters = dict(_converters)
        if converters:
            self._converters.update(converters)

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        headers = Headers(scope=scope)
        headerNames = headers.keys()
        extrasHeaders = filter.process(headerNames, 'extras')
        extras = {}
        for header_name in extrasHeaders:
            self._resolve_extras_value(extras, headers, header_name)

        scope['extras'] = extras
        ctx = get_async_context()
        ctx.webContext = WebContext({}, extras)
        return await ctx.run(self._app, scope, receive, send)

    def _resolve_extras_value(self, extras: dict, headers: Headers, name: str):
        key = pattern.sub(to_upper, name.replace('x-', ''))
        converter = self._converters.get(name)
        value = headers[name]
        if converter:
            value = converter(value)
        extras[key] = value


def to_upper(matched):
    text = matched.group(1)
    return text.upper()
