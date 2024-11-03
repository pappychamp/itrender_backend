from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

# paginationに対してのsqlalchemy拡張のチェックを無効
from fastapi_pagination.utils import disable_installed_extensions_check
from mangum import Mangum

from src.logs.logs_setting import logger

# from src.logs.sentry_setting import init_sentry
from src.routers import trend

disable_installed_extensions_check()


# init_sentry()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 全てのオリジンを許可する場合、または特定のオリジンに制限
    allow_credentials=True,
    allow_methods=["*"],  # 全てのHTTPメソッドを許可する場合
    allow_headers=["*"],  # 全てのヘッダーを許可する場合
)
app.include_router(trend.router)
add_pagination(app)

handler = Mangum(app)


@app.exception_handler(RequestValidationError)
async def custom_request_valid_handler(request: Request, exc: RequestValidationError):
    logger.error(f"{str(exc)}")
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
