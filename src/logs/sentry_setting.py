import os

import sentry_sdk
from sentry_sdk.integrations.asyncio import AsyncioIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from src.logs.logs_setting import logging

SENTRY_DSN = os.environ.get("SENTRY_DSN")


def init_sentry():
    # ログレベルをINFOに設定（INFO以上のメッセージがキャプチャされる）  # Sentryに送信するイベントのレベルをERRORに設定
    sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.INFO)
    # SentryのDSNを設定
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        integrations=[
            sentry_logging,
            AsyncioIntegration(),
        ],
    )
