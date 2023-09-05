#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.
from __future__ import annotations

from abc import ABC, abstractmethod
from io import BytesIO
from typing import Any, AsyncGenerator, Dict, Optional, Union

import aiohttp
from gql.transport import AsyncTransport
from gql.transport.aiohttp import AIOHTTPTransport
from graphql import DocumentNode, ExecutionResult, GraphQLSchema
from lru import LRU  # pylint: disable=no-name-in-module
from PIL import Image


class AioRequestAdapter(ABC):
    @abstractmethod
    async def fetch_bin(self, url: str) -> bytes:
        ...

    @abstractmethod
    def graphql_transport(self, url: str) -> Union[AsyncTransport, GraphQLSchema]:
        """Returns the transport or a local GraphQL schema to execute against."""
        ...

    async def fetch_image(self, url: str) -> Image.Image:
        return Image.open(BytesIO(await self.fetch_bin(url)))


class AioRequestAdapterImpl(AioRequestAdapter):
    def __init__(self, *, use_certifi_ssl=False):
        self.use_certifi_ssl = use_certifi_ssl

    async def fetch_bin(self, url: str) -> bytes:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, timeout=aiohttp.ClientTimeout(total=120)
            ) as resp:
                resp.raise_for_status()
                return await resp.read()

    def graphql_transport(self, url: str) -> AsyncTransport:
        if self.use_certifi_ssl:
            import certifi, ssl  # type: ignore  #  pylint: disable=no-name-in-module,no-member,import-error

            return AIOHTTPTransport(
                url=url, ssl=ssl.create_default_context(cafile=certifi.where())
            )
        return AIOHTTPTransport(url=url)


class CachedRequestAdapter(AioRequestAdapter):
    _request_adapter: AioRequestAdapter
    cache: LRU

    def __init__(self, cache_size: int, use_certifi_ssl=False):
        self._request_adapter = AioRequestAdapterImpl(use_certifi_ssl=use_certifi_ssl)
        self.use_certifi_ssl = use_certifi_ssl
        self.cache = LRU(cache_size)

    def flush_cache(self):
        self.cache.clear()

    async def fetch_bin(self, url: str) -> bytes:
        if url not in self.cache:
            self.cache[url] = await self._request_adapter.fetch_bin(url)
        return self.cache[url]

    def graphql_transport(self, url: str) -> "CachedAIOHTTPTransport":
        return CachedAIOHTTPTransport(url, self, use_certifi_ssl=self.use_certifi_ssl)


class CachedAIOHTTPTransport(AsyncTransport):
    _transport: AsyncTransport
    _cache: "CachedRequestAdapter"

    async def connect(self):
        return await self._transport.connect()

    async def close(self):
        return await self._transport.close()

    def __init__(self, url: str, cache: "CachedRequestAdapter", use_certifi_ssl=False):
        if use_certifi_ssl:
            import certifi, ssl  # type: ignore  #  pylint: disable=no-name-in-module,no-member,import-error

            self._transport = AIOHTTPTransport(
                url=url, ssl=ssl.create_default_context(cafile=certifi.where())
            )
        else:
            self._transport = AIOHTTPTransport(url=url)
        self._cache = cache

    async def execute(
        self,
        document: DocumentNode,
        variable_values: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None,
    ) -> ExecutionResult:
        cache_key = (document, variable_values, operation_name)
        if cache_key not in self._cache.cache:
            self._cache.cache[cache_key] = await self._transport.execute(
                document, variable_values, operation_name
            )
        return self._cache.cache[cache_key]

    def subscribe(
        self,
        document: DocumentNode,
        variable_values: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None,
    ) -> AsyncGenerator[ExecutionResult, None]:
        # We don't cache these.
        return self._transport.subscribe(document, variable_values, operation_name)
