from log4py import logging
from fastapi import FastAPI

from .tracing_context_middleware import TracingContextMiddleware

log = logging.getLogger('python.core.context')


def create_tracing(app: FastAPI):
    """创建构建extras的middleware
    """
    app.add_middleware(TracingContextMiddleware)
    log.info('创建extras context middleware完成')


__all__ = ['create_tracing']
