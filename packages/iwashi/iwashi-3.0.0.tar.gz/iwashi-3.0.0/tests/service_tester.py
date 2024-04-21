from typing import Iterable

import aiohttp

from iwashi.helper import BASE_HEADERS
from iwashi.visitor import Context, FakeVisitor, Result, Service


def iterable_eq(a: Iterable, b: Iterable) -> bool:
    # Compare two iterables for equality
    # ignoring the order of elements
    for item in a:
        if item not in b:
            return False
    for item in b:
        if item not in a:
            return False
    return True


async def _test_service(service: Service, correct_result: Result, *urls: str) -> None:
    # resolve id
    visitor = FakeVisitor()
    session = aiohttp.ClientSession(headers=BASE_HEADERS)
    for url in urls:
        context = Context(session=session, visitor=visitor)
        resolved_id = await service.resolve_id(context, url)
        assert (
            resolved_id == correct_result.id
        ), f"ID mismatch for {url} ({resolved_id} != {correct_result.id})"

    # visit
    for url in urls:
        result = await service.visit_url(session, url)
        assert result, f"Failed to visit {url}"
        assert (
            result.url == correct_result.url
        ), f"URL mismatch for {url} ({result.url} != {correct_result.url})"
        assert (
            result.service == correct_result.service
        ), f"Service mismatch for {url} ({result.service} != {correct_result.service})"
        assert (
            result.name == correct_result.name
        ), f"Name mismatch for {url} ({result.name} != {correct_result.name})"
        assert (
            result.description == correct_result.description
        ), f"Description mismatch for {url} ({result.description} != {correct_result.description})"
        assert (
            correct_result.profile_picture
            and result.profile_picture
            and (correct_result.profile_picture in result.profile_picture)
        ), f"Profile picture mismatch for {url} ({result.profile_picture} != {correct_result.profile_picture})"
        assert iterable_eq(
            result.links, correct_result.links
        ), f"Links mismatch for {url} ({result.links} != {correct_result.links})"
