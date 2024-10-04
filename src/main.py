from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

# paginationに対してのsqlalchemy拡張のチェックを無効
from fastapi_pagination.utils import disable_installed_extensions_check

from src.routers import trend

disable_installed_extensions_check()


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
