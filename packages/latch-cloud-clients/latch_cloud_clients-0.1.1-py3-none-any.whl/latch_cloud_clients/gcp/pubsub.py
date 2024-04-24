import asyncio
from dataclasses import dataclass
from typing import Any

import aiohttp
from google.api_core.exceptions import ServerError
from google.auth import default
from google.auth.transport import requests
from latch_data_validation.data_validation import validate


@dataclass(frozen=True)
class PubsubMessage:
    data: str
    attributes: dict[str, str]
    messageId: str
    publishTime: str
    orderingKey: str | None = None


@dataclass(frozen=True)
class SubscriptionMessage:
    ackId: str
    message: PubsubMessage
    # todo(taras): need to fix validation library so that optional fields are allowed
    # deliveryAttempt: Optional[int]


@dataclass(frozen=True)
class SubscriptionMessageResp:
    receivedMessages: list[SubscriptionMessage]


class AsyncPubsubClient:
    credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])

    def __init__(
        self, session: aiohttp.ClientSession, project_id: str, subscription: str
    ):
        self.project_id = project_id
        self.subscription = subscription
        self.api_url = f"https://pubsub.googleapis.com/v1/projects/{self.project_id}/subscriptions/{self.subscription}"
        self.session = session

    @staticmethod
    def get_auth_token():
        credentials = AsyncPubsubClient.credentials

        if credentials.token is None or credentials.expired:
            credentials.refresh(requests.Request())
        return credentials.token

    async def _make_api_request(self, method: str, endpoint: str, data: Any | None):
        async with self.session.request(
            method,
            endpoint,
            headers={"Authorization": f"Bearer {AsyncPubsubClient.get_auth_token()}"},
            data=data,
        ) as resp:
            if resp.status != 200:
                raise ServerError(await resp.text())
            return await resp.json()

    async def pull(
        self, max_messages: int = 20, timeout: int = 10
    ) -> list[SubscriptionMessage]:
        async with asyncio.timeout(timeout):
            body = await self._make_api_request(
                "POST",
                f"{self.api_url}:pull",
                {
                    "returnImmediately": False,
                    "maxMessages": max_messages,
                },
            )

            if "receivedMessages" not in body:
                return []
            return validate(body, SubscriptionMessageResp).receivedMessages

    async def acknowledge(self, ack_ids: list[str]):
        await self._make_api_request(
            "POST",
            f"{self.api_url}:acknowledge",
            {
                "ackIds": ack_ids,
            },
        )
