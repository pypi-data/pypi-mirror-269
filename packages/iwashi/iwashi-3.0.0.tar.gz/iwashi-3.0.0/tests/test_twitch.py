import pytest
from iwashi.service.twitch import Twitch
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_twitch():
    service = Twitch()
    correct = Result(
        service=service,
        id="thechief1114",
        url="https://www.twitch.tv/thechief1114",
        name="TheChief1114",
        description="I stream.",
        profile_picture="https://static-cdn.jtvnw.net/jtv_user_pictures/7a7f1681-f8ea-424d-bbce-38cac15e3328-profile_image-300x300.png",
        links={"https://twitter.com/The_Chief1114"},
    )
    await _test_service(service, correct, "https://www.twitch.tv/thechief1114")
