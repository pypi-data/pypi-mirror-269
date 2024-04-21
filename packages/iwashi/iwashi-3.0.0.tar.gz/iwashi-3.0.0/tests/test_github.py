import pytest
from iwashi.service.github import Github
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_github():
    service = Github()
    correct = Result(
        service=service,
        id="astral-sh",
        url="https://github.com/astral-sh",
        name="Astral",
        description="High-performance developer tools for the Python ecosystem.",
        profile_picture="https://avatars.githubusercontent.com/u/115962839",
        links={
            "https://twitter.com/astral_sh",
        },
    )
    await _test_service(
        service,
        correct,
        "https://github.com/astral-sh",
        "https://github.com/astral-sh/rye",
    )
