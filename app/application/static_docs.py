from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import HTMLResponse


def register_static_docs_routes(app: FastAPI) -> None:
    @app.get(path='/api/docs', include_in_schema=False)
    async def custom_swagger_ui_html() -> HTMLResponse:
        openapi_url: str = app.openapi_url if app.openapi_url else ''
        return get_swagger_ui_html(
            openapi_url=openapi_url,
            title=app.title + ' - Swagger UI',
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url='https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js',
            swagger_css_url='https://unpkg.com/swagger-ui-dist@5/swagger-ui.css',
        )

    @app.get(path=app.swagger_ui_oauth2_redirect_url, include_in_schema=False)  # type: ignore
    async def swagger_ui_redirect() -> HTMLResponse:
        return get_swagger_ui_oauth2_redirect_html()

    @app.get('/api/redoc', include_in_schema=False)
    async def redoc_html() -> HTMLResponse:
        openapi_url: str = app.openapi_url if app.openapi_url else ''
        return get_redoc_html(
            openapi_url=openapi_url,
            title=app.title + ' - ReDoc',
            redoc_js_url='https://unpkg.com/redoc@next/bundles/redoc.standalone.js',
        )
