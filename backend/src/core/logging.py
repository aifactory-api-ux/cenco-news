import structlog
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import contextvars

trace_id_var = contextvars.ContextVar("trace_id", default=None)


class TraceIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = request.headers.get("X-Trace-Id")
        if not trace_id:
            import uuid
            trace_id = str(uuid.uuid4())
        trace_id_var.set(trace_id)
        response = await call_next(request)
        response.headers["X-Trace-Id"] = trace_id
        return response


def get_logger(name: str = "app"):
    return structlog.get_logger(name)


structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict
)
