import os

import sentry_sdk
from sentry_sdk.integrations.asyncio import AsyncioIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from src.logs.logs_setting import logging

SENTRY_DSN = os.environ.get("SENTRY_DSN")


def init_sentry():
    # ログレベルをINFOに設定（INFO以上のメッセージがキャプチャされる）
    # # Sentryに送信するイベントのレベルをERRORに設定
    sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)
    # SentryのDSNを設定
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1,
        integrations=[
            # 422番のエラーはsentry_loggingでキャッチ
            # その他のエラーはFastApiIntegration,StarletteIntegrationでキャッチ
            # router内のエラーは500番エラーになるためFastApiIntegration,StarletteIntegrationでキャッチ(一応logger.infoでキャプチャはしている)
            sentry_logging,
            AsyncioIntegration(),
            StarletteIntegration(
                transaction_style="endpoint",
                failed_request_status_codes={403, *range(500, 599)},
                http_methods_to_capture=("GET",),
            ),
            FastApiIntegration(
                transaction_style="endpoint",
                failed_request_status_codes={403, *range(500, 599)},
                http_methods_to_capture=("GET",),
            ),
        ],
    )
