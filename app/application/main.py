from fastapi import FastAPI

from application.static_docs import register_static_docs_routes
from application.v1.name.handlers import router as name_router_v1

def create_app() -> FastAPI:
    fastapi_app = FastAPI(
        title='Name Origin API',
        debug=True,
        docs_url=None,
        redoc_url=None,
    )

    register_static_docs_routes(app=fastapi_app)

    fastapi_app.include_router(prefix='/v1', router=name_router_v1)

    return fastapi_app
