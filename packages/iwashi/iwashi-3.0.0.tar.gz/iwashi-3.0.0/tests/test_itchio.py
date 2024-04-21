import pytest
from iwashi.service.itchio import Itchio
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_itchio():
    service = Itchio()
    correct = Result(
        service=service,
        id="sebastian",
        url="https://sebastian.itch.io",
        name="Sebastian Lague",
        description=None,
        profile_picture="https://img.itch.zone/aW1nLzEwODg5MDY5LmpwZw==/80x80%23/rdXwL%2B.jpg",
        links={
            "https://twitter.com/SebastianLague",
            "https://itch.io/profile/sebastian",
            "https://www.youtube.com/channel/UCmtyQOKKmrMVaKuRXz02jbQ",
        },
    )
    await _test_service(
        service,
        correct,
        "https://itch.io/profile/sebastian",
        "https://sebastian.itch.io/",
        "https://sebastian.itch.io/tiny-chess-bots",
    )
