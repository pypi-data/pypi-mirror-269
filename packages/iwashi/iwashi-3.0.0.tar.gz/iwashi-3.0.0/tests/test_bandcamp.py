import pytest
from iwashi.visitor import Result
from iwashi.service.bandcamp import Bandcamp
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_bandcamp():
    service = Bandcamp()
    correct = Result(
        service=service,
        id="toxicholocaust",
        url="https://toxicholocaust.bandcamp.com",
        name="Toxic Holocaust",
        description="Toxic Thrash Metal\nEst. 1999",
        profile_picture="https://f4.bcbits.com/img/0032604396_21.jpg",
        links={"http://toxicholocaust.com"},
    )
    await _test_service(service, correct, "https://toxicholocaust.bandcamp.com")
