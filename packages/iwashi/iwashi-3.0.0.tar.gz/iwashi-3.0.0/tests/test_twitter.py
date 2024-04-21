import pytest
from iwashi.service.twitter import Twitter
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_twitter():
    service = Twitter()
    correct = Result(
        service=service,
        id="VALIGHT1",
        url="https://twitter.com/VALIGHT1",
        name="VALIGHT_YT",
        description="Hi, I'm Valight, a creative Fortnite mappeur\nWelcome to my twiter account.\nCODE VALIGHT",
        profile_picture="https://pbs.twimg.com/profile_images/1512100269831639049/R4AjwP-9_normal.jpg",
        links={"https://youtube.com/channel/UCDRIfKm06-e1dwSbnU1H9Rw"},
    )
    await _test_service(service, correct, "https://twitter.com/VALIGHT1")
