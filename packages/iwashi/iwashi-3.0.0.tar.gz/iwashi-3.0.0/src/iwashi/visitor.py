from __future__ import annotations

import abc
from datetime import timedelta
import re
from dataclasses import dataclass, field
from typing import List, Optional, Protocol, Set

import aiohttp

from iwashi.throttle import Throttle

HTTP_REGEX = "(https?://)?(www.)?"


@dataclass
class Result:
    service: Service
    id: str
    url: str
    name: Optional[str]
    description: Optional[str]
    profile_picture: Optional[str]

    children: List[Result] = field(default_factory=list)
    links: Set[str] = field(default_factory=set)

    def to_list(self) -> List[Result]:
        links: List[Result] = [self]
        for child in self.children:
            links.extend(child.to_list())
        return links


class Visitor(Protocol):
    async def visit(self, url: str, context: Context) -> Result | None:
        ...

    def mark_visited(self, url: str) -> None:
        ...

    def enqueue_visit(self, url: str, context: Context) -> None:
        ...


class FakeVisitor(Visitor):
    def __init__(self):
        self.queue: List[str] = []

    async def visit(self, url, context, **kwargs):
        raise NotImplementedError

    async def tree(self, url, context, **kwargs):
        raise NotImplementedError

    def enqueue_visit(self, url, context):
        self.queue.append(url)

    def mark_visited(self, url):
        raise NotImplementedError


@dataclass
class Context:
    session: aiohttp.ClientSession
    visitor: Visitor
    parent: Optional[Context] = None
    result: Optional[Result] = None

    def create_result(
        self,
        service: Service,
        id: str,
        url: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        profile_picture: Optional[str] = None,
    ) -> Result:
        self.result = Result(
            service=service,
            id=id,
            url=url,
            name=name,
            description=description,
            profile_picture=profile_picture,
        )

        if self.parent and self.parent.result:
            self.parent.result.children.append(self.result)

        return self.result

    def link(self, url: str) -> None:
        if self.result is None:
            raise ValueError("Result is not created yet")
        self.result.links.add(url)

    def mark_visited(self, url: str) -> None:
        self.visitor.mark_visited(url)

    def create_context(self) -> Context:
        return Context(session=self.session, visitor=self.visitor, parent=self)

    def enqueue_visit(self, url: str) -> None:
        if self.result is not None:
            self.link(url)
        self.visitor.enqueue_visit(url, self)


class Service(abc.ABC):
    throttle: Throttle

    def __init_subclass__(cls) -> None:
        cls.throttle = Throttle(timedelta(seconds=5))
        return super().__init_subclass__()

    def __init__(self, name: str, regex: re.Pattern):
        self.name = name
        self.regex = regex

    def match(self, url, context: Context) -> Optional[re.Match]:
        return self.regex.match(url)

    async def resolve_id(self, context: Context, url: str) -> str | None:
        match = self.regex.search(url)
        return match and match.group("id")

    @abc.abstractmethod
    async def visit(self, context: Context, id: str) -> Optional[Result]:
        raise NotImplementedError()

    async def visit_url(
        self, session: aiohttp.ClientSession, url: str
    ) -> Optional[Result]:
        async with self.throttle:
            visitor = FakeVisitor()
            context = Context(session=session, visitor=visitor)
            id = await self.resolve_id(context, url)
            if id is None:
                return None
            await self.visit(context, id)
            return context.result
