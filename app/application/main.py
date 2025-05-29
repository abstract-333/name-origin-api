from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from application.static_docs import register_static_docs_routes
from application.v1.name.handlers import router as name_router_v1
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
    """Create FastAPI application.

    Returns:
        FastAPI: FastAPI application instance
    """
    app = FastAPI(
        title='Name Origin API',
        description='API for getting name origins and popular names by country',
        version='1.0.0',
        lifespan=lifespan,
        docs_url=None,
        redoc_url=None,
        default_response_class=ORJSONResponse,
    )

    # Add middleware
    app.add_middleware(BrotliMiddleware)

    # Register routes
    app.include_router(name_router_v1, prefix='/api/v1')

    # Register static docs routes
    register_static_docs_routes(app)

    return app
