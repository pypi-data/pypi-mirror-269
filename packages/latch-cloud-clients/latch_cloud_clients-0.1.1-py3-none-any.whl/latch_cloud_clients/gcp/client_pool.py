from asyncio import gather
from asyncio.locks import BoundedSemaphore
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass

import aiohttp
from opentelemetry.trace import get_tracer

from .pubsub import AsyncPubsubClient
from .storage import AsyncStorageClient

tracer = get_tracer(__name__)


class AsyncGCPClient:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    def __aexit__(self, exc_type, exc_val, exc_tb):
        return self.session.__aexit__(exc_type, exc_val, exc_tb)

    def storage_client(self):
        return AsyncStorageClient(self.session)

    def pubsub_client(self, project_id: str, subscription: str):
        return AsyncPubsubClient(self.session, project_id, subscription)


@dataclass
class ClientList:
    sema: BoundedSemaphore
    client_add_sema: BoundedSemaphore
    clients: list[AsyncGCPClient]


class AsyncGCPClientPool:
    max_clients: int | None = None
    client_list: ClientList | None = None

    async def open(self, max_clients: int):
        with tracer.start_as_current_span(
            "open pool", attributes={"max_clients": max_clients}
        ):
            self.max_clients = max_clients
            self.client_list = ClientList(
                sema=BoundedSemaphore(self.max_clients),
                client_add_sema=BoundedSemaphore(1),
                clients=[],
            )

    async def close(self):
        with tracer.start_as_current_span("close pool"):
            if self.max_clients is None or self.client_list is None:
                raise RuntimeError("Pool not open")

            close_tasks = []
            for client in self.client_list.clients:
                close_tasks.append(client.__aexit__(None, None, None))

            await gather(*close_tasks)
            self.client_list = None
            self.max_clients = None

    @asynccontextmanager
    async def gcp_client(self) -> AsyncGenerator[AsyncGCPClient, None]:
        with tracer.start_as_current_span("get client") as s:
            if self.max_clients is None or self.client_list is None:
                raise RuntimeError("Pool not open")

            async with self.client_list.sema:
                async with self.client_list.client_add_sema:
                    if len(self.client_list.clients) == 0:
                        with tracer.start_as_current_span(
                            "create gcp client",
                        ):
                            http_session = await aiohttp.ClientSession().__aenter__()
                            client = AsyncGCPClient(http_session)
                    else:
                        client = self.client_list.clients.pop()

                try:
                    yield client
                finally:
                    self.client_list.clients.append(client)
                    s.set_attributes(
                        {
                            "client_count": len(self.client_list.clients),
                        }
                    )


gcp_pool = AsyncGCPClientPool()
