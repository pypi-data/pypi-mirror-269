import contextvars

from typing import Dict


class WebContext:
    def __init__(self, principal: Dict[str, any], extras: Dict[str, any]):
        self.principal = principal
        self.extras = extras


OpenTracing = Dict[str, any]


class AsyncContext:
    def __init__(self):
        self._web_context = contextvars.ContextVar('webContext')
        self._open_tracing = contextvars.ContextVar('tracing')
        self._generic = contextvars.ContextVar('generic')
        self._tenant = contextvars.ContextVar('tenant')

    def run(self, fn, *args, **kwargs):
        curr_ctx = contextvars.copy_context()
        return curr_ctx.run(fn, *args, **kwargs)

    def get(self, key: str):
        data: Dict[str, any] = self._generic.get(None)
        if not data:
            return None
        return data.get(key, None)

    def set(self, key: str, value):
        data: Dict[str, any] = self._generic.get(None)
        if not data:
            if value is None:
                # 空值什么也不做
                return
            data = {}
            self._generic.set(data)
        data[key] = value
        return value

    @ property
    def webContext(self) -> WebContext:
        return self._web_context.get(None)

    @ webContext.setter
    def webContext(self, ctx: WebContext):
        return self._web_context.set(ctx)

    @ property
    def tracing(self) -> OpenTracing:
        return self._open_tracing.get(None)

    @ tracing.setter
    def tracing(self, tracing: OpenTracing):
        self._open_tracing.set(tracing)

    @ property
    def tenant_id(self) -> int:
        # 优先使用独立设置的tenant
        tenant_id_ = self._tenant.get(None)
        if tenant_id_ is not None:
            return tenant_id_

        # web上的tenant
        ctx = self.webContext
        if ctx:
            if ctx.principal:
                return ctx.principal['tenantId']
            elif ctx.extras:
                return ctx.extras['tenantId']
        return None

    @ tenant_id.setter
    def tenant_id(self, id: int):
        if not isinstance(id, int):
            raise Exception(id, '租户id必须是整数')
        self._tenant.set(id)


__context: AsyncContext = None


def get_async_context():
    global __context
    if not __context:
        __context = AsyncContext()
    return __context
