from __future__ import annotations  # remove when dropping 3.8 support

from typing import Any

from whos_there.senders.base import Sender


class SlackSender(Sender):
    def __init__(self, webhook_url: str, channel: str, user_mentions: list[str] | None = None) -> None:
        """Initialize the Slack sender.

        Args:
            webhook_url: The Slack webhook URL.
            channel: The Slack channel name.
            user_mentions: The list of users to mention.
        """
        super().__init__()
        self.webhook_url = webhook_url
        self.channel = channel
        self.user_mentions = " ".join(user_mentions) if user_mentions else []

    def send(self, text: str) -> Any:
        data = {
            "username": "Knock Knock",
            "channel": self.channel,
            "link_names": 1,
            "icon_emoji": ":clapper:",  # ":tada:"
            "text": f"{text} {self.user_mentions}",
        }
        return self._send_json(self.webhook_url, data)
