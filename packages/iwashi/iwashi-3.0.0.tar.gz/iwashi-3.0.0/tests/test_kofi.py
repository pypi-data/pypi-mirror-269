import pytest
from iwashi.service.kofi import Kofi
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_itchio():
    service = Kofi()
    correct = Result(
        service=service,
        id="sebastianlague",
        url="https://ko-fi.com/sebastianlague",
        name="Sebastian Lague",
        description=None,
        profile_picture="https://storage.ko-fi.com/cdn/useruploads/d424f5dc-43e9-4791-bf26-53fe84637888_703f1344-ba07-467d-956c-539509201e78.png",
        links={
            "https://www.youtube.com/@SebastianLague",
        },
    )
    await _test_service(
        service,
        correct,
        "https://ko-fi.com/sebastianlague",
        "https://ko-fi.com/sebastianlague/shop",
    )
