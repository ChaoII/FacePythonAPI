from base.log import logger
from base.config import settings
from fastapi import FastAPI, applications, Request
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from tortoise.contrib.fastapi import register_tortoise
from slowapi import Limiter, _rate_limit_exceeded_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.docs import get_swagger_ui_oauth2_redirect_html


def register_offline_docs(app: applications):
    def custom_swagger_ui_html(*args, **kwargs):
        return get_swagger_ui_html(
            *args,
            **kwargs,
            swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui/swagger-ui.css",
            swagger_favicon_url="/static/swagger-ui/favicon.png"
        )

    def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    def redoc_html(*args, **kwargs):
        return get_redoc_html(
            *args,
            **kwargs,
            redoc_js_url="/static/redoc/bundles/redoc.standalone.js",
            redoc_favicon_url="/static/redoc/img/favicon.png",
        )

    app.get_swagger_ui_html = custom_swagger_ui_html
    app.get_swagger_ui_oauth2_redirect_html = swagger_ui_redirect
    app.get_redoc_html = redoc_html


def register_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        **settings.CORS
    )


def register_orm(app: FastAPI):
    register_tortoise(
        app,
        config={
            'connections': {
                'default': settings.DB_URL
            },
            'apps': {
                'models': {
                    "models": ["models.models"],
                    'default_connection': 'default',
                }
            },
            "use_tz": False,
            "timezone": "Asia/Shanghai",
        }
    )


def register_limit(app: FastAPI):
    # 实例化一个limiter对象，根据客户端地址进行限速
    limiter = Limiter(key_func=get_remote_address)
    # 指定FastApi的限速器为limiter
    app.state.limiter = limiter
    # 指定FastApi的异常拦截器
    return limiter


def register_exception(app: FastAPI):
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def register_middleware(app: FastAPI):
    """
    请求响应拦截 hook
    :param app:
    :return:
    """

    @app.middleware("http")
    async def logger_request(request: Request, call_next):
        logger.info(f"|访问记录:{request.method}  |url:{request.url}  |IP:{request.client.host}")
        response = await call_next(request)
        return response
