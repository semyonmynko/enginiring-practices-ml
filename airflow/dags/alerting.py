import html
import logging

import requests
from airflow.hooks.base import BaseHook


def on_failure_callback(context):
    logger = logging.getLogger("telegram_alert")

    try:
        conn = BaseHook.get_connection("telegram_alerts")
        bot_token = conn.password or conn.login
        chat_id = (conn.extra_dejson or {}).get("chat_id")

        ti = context["task_instance"]
        dag_id = context["dag"].dag_id
        task_id = ti.task_id
        error = str(context.get("exception") or "Unknown error")
        log_url = ti.log_url

        dag_id = html.escape(dag_id)
        task_id = html.escape(task_id)
        error = html.escape(error)
        log_url = html.escape(log_url, quote=True)

        message = (
            f"🚨 <b>Airflow Task Failed</b>\n"
            f"<b>DAG:</b> {dag_id}\n"
            f"<b>Task:</b> {task_id}\n"
            f"<b>Error:</b> {error}\n"
        )

        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()

        logger.info("Telegram alert sent successfully")

    except Exception as e:
        logger.error(f"Failed to send Telegram alert: {e}")
