import re

from starlette.datastructures import Headers
from starlette.types import ASGIApp, Receive, Scope, Send
from ..context import get_async_context, header_filter as filter

pattern = re.compile('-([a-z])', re.IGNORECASE)


class TracingContextMiddleware:
    def __init__(self, app: ASGIApp):
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        headers = Headers(scope=scope)
        headerNames = headers.keys()
        tracingHeaders = filter.process(headerNames, 'tracing')
        tracing = {}
        for header_name in tracingHeaders:
            tracing[header_name] = headers[header_name]
        scope['tracing'] = tracing

        ctx = get_async_context()
        ctx.tracing = tracing
        return await ctx.run(self._app, scope, receive, send)
