import os
from discord import SyncWebhook


def send_tip(tip_text: str) -> None:
    """
    使用 Discord Webhook 發送每日小技巧
    """
    webhook_url = os.environ['DISCORD_WEBHOOK_URL']
    webhook = SyncWebhook.from_url(webhook_url)
    webhook.send(tip_text)

    print("Daily tip sent to Discord!")