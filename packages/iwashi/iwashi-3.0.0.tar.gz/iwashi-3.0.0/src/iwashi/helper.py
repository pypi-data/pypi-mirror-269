from __future__ import annotations
import asyncio
import random
import re
import string
import time
from typing import Any, Callable

from loguru import logger

from .visitor import Result

USER_AGENT = "Profile Link Generator (https://github.com/am230/iwashi)"
BASE_HEADERS = {"User-Agent": USER_AGENT}
HTTP_REGEX = "(https?://)?(www.)?"
DEBUG = False


def print_result(
    result: Result, indent_level=0, print: Callable[[str], Any] = print
) -> None:
    indent = indent_level * "    "
    print(f"{indent}{result.service.name}")
    print(f"{indent}|id    : {result.id}")
    print(f"{indent}│url   : {result.url}")
    print(f"{indent}│name  : {result.name}")
    print(f"{indent}│links : {result.links}")
    if result.description:
        print(f"{indent}│description: " + result.description.replace("\n", "\\n"))
    for child in result.children:
        print_result(child, indent_level + 1, print)


def random_string(length: int) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


URL_NORMALIZE_REGEX = r"(?P<protocol>https?)?:?\/?\/?(?P<domain>[^.]+\.[^\/]+)(?P<path>[^?#]+)?(?P<query>.+)?"


def normalize_url(url: str, https: bool = True) -> str | None:
    url = str(url).strip()
    match = re.match(URL_NORMALIZE_REGEX, url)
    if match is None:
        return None
    protocol = match.group("protocol") or "https"
    domain = match.group("domain")
    path = match.group("path") or ""
    query = match.group("query") or ""
    if https:
        protocol = "https"
    return f"{protocol}://{domain}{path}{query}"


def retry(
    max_retry: int,
    retry_interval: int = 0,
    retry_on: Callable[[Exception], bool] = lambda _: True,
) -> Callable[..., Any]:
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(max_retry):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if not retry_on(e):
                        raise e
                    logger.debug(f"Retrying {func.__name__} ({i + 1}/{max_retry})")
                    time.sleep(retry_interval)
                    continue
            raise Exception(
                f"Failed to execute {func.__name__} after {max_retry} retries"
            )

        return wrapper

    return decorator


def retry_async(
    max_retry: int,
    retry_interval: int = 0,
    retry_on: Callable[[Exception], bool] = lambda _: True,
) -> Callable[..., Any]:
    def decorator(func):
        async def wrapper(*args, **kwargs):
            e: Exception | None = None
            for i in range(max_retry):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if not retry_on(e):
                        raise e
                    logger.debug(f"Retrying {func.__name__} ({i + 1}/{max_retry})")
                    await asyncio.sleep(retry_interval)
                    continue
            raise Exception(
                f"Failed to execute {func.__name__} after {max_retry} retries"
            )

        return wrapper

    return decorator


def cache(func: Callable[..., Any]) -> Callable[..., Any]:
    cache = {}

    def wrapper(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        if key in cache:
            return cache[key]
        result = func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper


def cache_async(func: Callable[..., Any]) -> Callable[..., Any]:
    cache = {}

    async def wrapper(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        if key in cache:
            return cache[key]
        result = await func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper


class Traverser[T]:
    def __init__(self, value: T | None = None):
        self.value = value

    def map[V](self, func: Callable[[T], V], default: V | None = None) -> Traverser[V]:
        if self.value is None:
            return TRAVERSE_NONE
        value = func(self.value)
        if value is None:
            return Traverser(default)
        return Traverser(value)

    def get(self, default: T | None = None) -> T | None:
        if self.value is None:
            return default
        return self.value

    def unwrap(self) -> T:
        if self.value is None:
            raise ValueError("Value is None")
        return self.value

    def is_none(self) -> bool:
        return self.value is None


TRAVERSE_NONE = Traverser(None)


def traverse[T](value: T | None) -> Traverser[T]:
    """
    Traverse a value that may be None.
    """
    return Traverser(value)
