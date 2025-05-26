from contextlib import asynccontextmanager
from typing import cast
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from punq import Container

from application.static_docs import register_static_docs_routes
from application.v1.name.handlers import router as name_router_v1
from logic.init import init_container
from settings.config import Config
from brotli_asgi import BrotliMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application.

    Args:
        app: FastAPI application instance
    """
    # Startup
    yield
    # Shutdown


def create_app() -> FastAPI:
    container: Container = init_container()
    config = cast(Config, container.resolve(Config))

    fastapi_app = FastAPI(
        title='Name Origin API',
        debug=config.debug,
        docs_url=None,
        redoc_url=None,
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    # Add gzip compression middleware
    fastapi_app.add_middleware(
        middleware_class=BrotliMiddleware,
        quality=6,
        minimum_size=1000,
    )

    register_static_docs_routes(app=fastapi_app)

    fastapi_app.include_router(prefix='/v1', router=name_router_v1)

    return fastapi_app
