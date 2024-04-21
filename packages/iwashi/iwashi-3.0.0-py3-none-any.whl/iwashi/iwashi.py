import asyncio
from typing import List, MutableSet, NamedTuple, Optional
import aiohttp
from loguru import logger
from .helper import BASE_HEADERS, DEBUG, normalize_url
from .visitor import Context, Result, Service, Visitor
from .service import SERVICES


class Identifier(NamedTuple):
    site: str
    id: str


class Iwashi(Visitor):
    def __init__(self) -> None:
        self.services: List[Service] = []
        self.visited_urls: MutableSet[str] = set()
        self.visited_ids: MutableSet[Identifier] = set()
        self.tasks: List[asyncio.Task] = []
        self.session = aiohttp.ClientSession(headers=BASE_HEADERS)

    def add_service(self, service: Service) -> None:
        self.services.append(service)

    def is_visited(self, url: str) -> bool:
        return url in self.visited_urls

    def mark_visited(self, url: str):
        self.visited_urls.add(url)

    async def tree(self, url: str, context: Optional[Context] = None) -> Result | None:
        context = context or Context(session=self.session, visitor=self)
        context = context.create_context()
        result = await self.visit(url, context)
        while self.tasks:
            await self.tasks.pop()

        return result

    def enqueue_visit(self, url: str, context: Context) -> None:
        coro = self.visit(url, context)
        task = asyncio.create_task(coro)
        self.tasks.append(task)

    async def visit(self, url: str, context: Context) -> Optional[Result]:
        normalized_url = normalize_url(url)
        if normalized_url is None:
            return None
        context = context.create_context()
        if self.is_visited(normalized_url):
            return None
        for service in self.services:
            match = service.match(normalized_url, context)
            if match is None:
                continue

            try:
                id = await service.resolve_id(context, normalized_url)
                if id is None:
                    continue
                identifier = Identifier(site=service.name, id=id)
                if identifier in self.visited_ids:
                    continue
                self.visited_ids.add(identifier)
                async with service.throttle:
                    await service.visit(context, id)
            except Exception as e:
                logger.warning(
                    f"[Service Error] {service.name} failed to visit {normalized_url}"
                )
                logger.exception(e)
                if DEBUG:
                    raise e
                continue
            self.mark_visited(normalized_url)
            break
        else:
            self.mark_visited(normalized_url)
            if await self.try_redirect(normalized_url, context):
                return context.result
            else:
                logger.warning(f"[No Service] No service matched {normalized_url}")

        return context.result

    async def try_redirect(self, url: str, context: Context) -> bool:
        try:
            res = await context.session.get(
                url, headers=BASE_HEADERS, allow_redirects=True, timeout=5
            )
            res.raise_for_status()
        except aiohttp.ClientError as e:
            logger.exception(e)
            logger.warning(f"[Redirect] failed to redirect {url}")
            return False
        except asyncio.TimeoutError as e:
            logger.exception(e)
            logger.warning(f"[Redirect] failed to redirect {url}")
            return False
        new_url = str(res.url)
        if new_url == url:
            return False
        context.enqueue_visit(new_url)
        logger.info(f"[Redirect] {url} -> {new_url}")
        return True


def get_iwashi():
    iwashi = Iwashi()

    for service in SERVICES:
        iwashi.add_service(service)

    return iwashi


async def tree(url: str, iwashi: Optional[Iwashi] = None) -> Optional[Result]:
    iwashi = iwashi or get_iwashi()
    return await iwashi.tree(url)
