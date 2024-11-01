import argparse

from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
import uvicorn,http,asyncio

from fastapi import FastAPI
from configs.server_config import OPEN_CROSS_DOMAIN


from server.api_server.chatreport_routes import chatreport_router

from server.utils.serverUtils import MakeFastAPIOffline

from mq_consumer import async_consume_messages


def create_app(run_mode: str = None):
    app = FastAPI(
        title = "数智助手 API Server",
        version = 'v1.0.0'
    )
    MakeFastAPIOffline(app)
    # Add CORS middleware to allow all origins
    # 在config.py中设置OPEN_DOMAIN = True，允许跨域
    # set OPEN_DOMAIN = True in config.py to allow cross-domain
    if OPEN_CROSS_DOMAIN:
        app.add_middleware(
            CORSMiddleware,
            allow_origins = ["*"],
            allow_credentials = True,
            allow_methods = ["*"],
            allow_headers = ["*"],
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, e: Exception):
        return JSONResponse(
            status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )

    @app.get("/", summary = "swagger 文档", include_in_schema = False)
    async def document():
        return RedirectResponse(url = "/docs")


    @app.on_event("startup")
    async def startup_event():
        # 创建异步任务来消费消息
        await async_consume_messages()
        print("Starting HTTP server...")



    app.include_router(chatreport_router)





    return app


def run_api(host, port, **kwargs):

    if kwargs.get("ssl_keyfile") and kwargs.get("ssl_certfile"):
        uvicorn.run(app,
                    host = host,
                    port = port,
                    ssl_keyfile = kwargs.get("ssl_keyfile"),
                    ssl_certfile = kwargs.get("ssl_certfile")
                    )
    else:
        uvicorn.run(app, host = host, port = port)

app = create_app()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = 'cestc-smartassistant',
                                     description = '数智助手服务')
    parser.add_argument("--host", type = str, default = "0.0.0.0")
    parser.add_argument("--port", type = int, default = 7788)
    parser.add_argument("--ssl_keyfile", type = str)
    parser.add_argument("--ssl_certfile", type = str)
    # 初始化消息
    args = parser.parse_args()
    args_dict = vars(args)
    run_api(host = args.host,
            port = args.port,
            ssl_keyfile = args.ssl_keyfile,
            ssl_certfile = args.ssl_certfile,
            )
